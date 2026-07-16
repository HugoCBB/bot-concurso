from typing import List, Dict
from .transform import clean_contest, parse_date_for_sorting
import asyncio
import httpx
from playwright.async_api import Page
from infra.s3_client import get_s3_client
from modules.config.config import setting
from slugify import slugify

global __s3
__s3 = get_s3_client()

url = "https://www.pciconcursos.com.br/concursos/"


async def get_contest(page: Page, queue: asyncio.Queue) -> List[Dict]:
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


async def download_pdf(url: str, orgao: str) -> str:
    filename = f"{slugify(orgao)}/{slugify(url.split('/')[-1].replace('.pdf', ''))}.pdf" 
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        await upload_to_s3(filename, response)

        s3_url = f"{setting.s3_endpoint}/{setting.s3_bucket}/{filename}"
        return s3_url
    except Exception as e:
        print(f"erro ao baixar pdf: {e}")

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