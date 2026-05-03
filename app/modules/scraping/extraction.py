from typing import List, Dict
import re
from .transform import clean_contest, parse_date_for_sorting
import asyncio
import httpx
from playwright.async_api import Page
from modules.utils.file_dirs import FILE_PDF_DIR

url = "https://www.pciconcursos.com.br/concursos/"


async def get_contest(page: Page, queue: asyncio.Queue) -> List[Dict]:
        await page.goto(url)
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
    orgao_clean = re.sub(r'[/\\:*?"<>|]', '_', orgao)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    filename = f"{FILE_PDF_DIR}/{orgao_clean}_{url.split('/')[-1]}"
    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"Pdf salvo: {filename}")
    return filename