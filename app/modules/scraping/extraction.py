from typing import List, Dict
from .transform import clean_contest, parse_date_for_sorting
import asyncio
import httpx
from playwright.async_api import Page
from infra.s3_client import get_s3_client
from modules.config.config import setting
from slugify import slugify
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

global __s3
__s3 = get_s3_client()

url = "https://www.pciconcursos.com.br/concursos/"


async def get_contest(page: Page, queue: asyncio.Queue, worker_count: int = 1) -> List[Dict]:
        await page.goto(url, wait_until="domcontentloaded")
        elements = await page.locator("div .da, .ea, .na").all()

        contest_data = []
        for el in elements:
            text = await el.inner_text()
            link = await el.get_attribute("data-url")
            contest_data.append(f"{text}\n{link}")

        data = clean_contest(contest_data)
        ordered_data = sorted(data, key=lambda x: parse_date_for_sorting(x['data_limite']))

        for contest in ordered_data:
            await queue.put(contest)

        # uma sentinela por worker para encerrar todos os consumidores
        for _ in range(worker_count):
            await queue.put(None)


async def get_pdf_links(page: Page, url: str) -> list[str]:
    await page.goto(url)
    elements = await page.locator(".pdf a").all()
    
    links = []
    for el in elements:
        href = await el.get_attribute("href")
        if href and href.endswith(".pdf"):
            links.append(href)
    
    return links

async def process_contest(contest: Dict, browser, sem: asyncio.Semaphore) -> Dict | None:
    """Processa um concurso de forma isolada: uma falha aqui nao derruba o batch."""
    async with sem:
        try:
            page = await browser.new_page()
            try:
                pdf_links = await get_pdf_links(page, contest["link"])
            finally:
                await page.close()

            results = await asyncio.gather(
                *[download_pdf(link, contest["orgao"]) for link in pdf_links],
                return_exceptions=True,
            )

            s3_urls = []
            for link, res in zip(pdf_links, results):
                if isinstance(res, Exception):
                    logger.error("Erro no PDF %s (%s): %s", link, contest["orgao"], res)
                elif res:
                    s3_urls.append(res)

            contest["edital_urls"] = s3_urls
            return contest
        except Exception as e:
            logger.error("Falhou concurso %s: %s", contest.get("orgao"), e)
            return None


async def download_pdf(url: str, orgao: str, max_retries: int = 3) -> str:
    filename = f"{slugify(orgao)}/{slugify(url.split('/')[-1].replace('.pdf', ''))}.pdf"

    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url)
                response.raise_for_status()

            await upload_to_s3(filename, response)
            return f"{setting.s3_endpoint}/{setting.s3_bucket}/{filename}"
        except Exception as e:
            last_exc = e
            if attempt < max_retries:
                wait = 2 ** (attempt - 1) 
                logger.warning(
                    "Falha ao baixar %s (tentativa %d/%d): %s. Retentando em %ds",
                    url, attempt, max_retries, e, wait,
                )
                await asyncio.sleep(wait)

    raise last_exc

async def upload_to_s3(filename: str, response):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: __s3.put_object(
            Bucket=setting.s3_bucket,
            Key=filename,
            Body=response.content,
            ContentType="application/pdf",
        )
    )


def s3_key_from_url(s3_url: str) -> str:
    """Recover the object key from a stored S3 URL (endpoint/bucket/<key>)."""
    return s3_url.split(f"/{setting.s3_bucket}/", 1)[-1]


async def delete_from_s3(s3_url: str):
    """Delete a single PDF object from S3 given its stored URL."""
    key = s3_key_from_url(s3_url)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: __s3.delete_object(Bucket=setting.s3_bucket, Key=key),
    )