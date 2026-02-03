from playwright.async_api import async_playwright
from typing import List, Dict
import asyncio

url = "https://www.pciconcursos.com.br/concursos/"


async def get_contest() -> List[Dict]:
    async with async_playwright() as p:
        try:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()

            await page.goto(url)
            contest = await page.locator("div .da, .ea, .na").all_inner_texts()

            return contest

        except Exception as e:
            print(e)
        finally:
            await browser.close()

def clean_contest(contest: List[str]) -> List:
    clean_data = []
    for item in contest:
        
        parts = item.split("\n")
        clean_parts = [p.strip() for p in parts if p.strip()]

        if not clean_parts:
            continue

        mapper = {
            "orgao": clean_parts[0],
            "info":clean_parts[1],
            "cargo":clean_parts[2],
            "nivel": clean_parts[3],
            "data_limite": clean_parts[4]
        }

        clean_data.append(mapper)    
    return clean_data

async def run():
    data = await get_contest()
    clean_data = clean_contest(data)
    print(clean_data[0])

if __name__ == "__main__":
    asyncio.run(run())