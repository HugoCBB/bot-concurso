from playwright.async_api import async_playwright
import re
from typing import List, Dict
import asyncio


url = "https://www.pciconcursos.com.br/concursos/"


class Extraction:

    @staticmethod
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

    @staticmethod
    def clean_contest(contest: List[str]) -> List:
        clean_data = []
        for item in contest:
            
            parts = item.split("\n")
            clean_parts = [p.strip() for p in parts if p.strip()]

            if not clean_parts:
                continue
            if len(clean_parts) < 5:
                continue
            

            mapper = {
                "orgao": clean_parts[0],
                "info":clean_parts[1],
                "cargo":clean_parts[2],
                "nivel": clean_parts[3],
                "data_limite": Extraction.get_clean_data(clean_parts)
            }

            clean_data.append(mapper)    
        return clean_data
    
    @staticmethod
    def get_clean_data(clean_parts: List) -> str:
        raw_date = " ".join(clean_parts[4:])
        date_pattern = r"\d{2}/\d{2}(?:/\d{4})?"

        interval_match = re.search(f"({date_pattern})\s+a\s+({date_pattern})", raw_date)

        if interval_match:
            final_date = interval_match.group(0)
        else:
            single_match = re.search(date_pattern, raw_date)
            if single_match:
                final_date = single_match.group(0)
            else:
                final_date = raw_date

        return final_date


        
    
    @staticmethod
    async def run():
        data = await Extraction.get_contest()
        clean_data = Extraction.clean_contest(data)
        print(clean_data[0:10])

if __name__ == "__main__":
    asyncio.run(Extraction.run())