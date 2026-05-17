import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.scraping.extraction import get_contest, get_pdf_links, download_pdf
from infra.redis_client import save_contests
from playwright.async_api import async_playwright, Browser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

async def consumer(queue: asyncio.Queue, browser: Browser):
    contests_process = []
    while True:
        contest = await queue.get()
        
        if contest is None:
            break
        
        logger.info(f"Processando pdf: {contest['orgao']}")
        page = await browser.new_page()
        pdf_links = await get_pdf_links(page, contest["link"])
        await page.close()
        
        s3_urls = []
        for link in pdf_links:
            try:
                s3_url = await download_pdf(link, contest["orgao"])
                s3_urls.append(s3_url)
            except Exception as e:
                logger.error(f"Erro no upload do PDF {link}: {e}")

        contest["edital_urls"] = s3_urls 
        contests_process.append(contest)
        await save_contests(contests_process)
        queue.task_done()
        
    logger.info(f"{len(contests_process)} concursos salvos no redis")
        

async def main():
    queue = asyncio.Queue()
    
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        
        await asyncio.gather(            
            get_contest(page, queue),
            consumer(queue, browser)
        )
    
asyncio.run(main())

 
