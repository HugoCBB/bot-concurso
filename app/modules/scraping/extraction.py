from playwright.async_api import async_playwright
import re
from typing import List, Dict
from datetime import datetime, date

url = "https://www.pciconcursos.com.br/concursos/"


def clean_contest(contest: List[str]) -> List:
    clean_data = []
    for item in contest:
            
        parts = item.split("\n")
        clean_parts = [p.strip() for p in parts if p.strip()]
        
        if not clean_parts:
            continue
        
        if len(clean_parts) < 4:
            continue
            
        middle_parts = clean_parts[1:-1]
        
        if len(middle_parts) > 0 and len(middle_parts[0]) == 2 and middle_parts[0].isalpha() and middle_parts[0].isupper():
            uf = middle_parts[0]
            middle_parts = middle_parts[1:]
        else:
            uf = ""
            
        info = middle_parts[0] if len(middle_parts) > 0 else ""
        if uf:
            info = f"{uf} - {info}"
            
        cargo = middle_parts[1] if len(middle_parts) > 1 else ""
        nivel = middle_parts[2] if len(middle_parts) > 2 else ""

        data_limite_str = get_clean_data(clean_parts)
        data_limite_obj = parse_date_for_sorting(data_limite_str)

        if data_limite_obj < datetime.now():
            continue

        mapper = {
            "orgao": clean_parts[0],
            "info": info,
            "cargo": cargo,
            "nivel": nivel,
            "data_limite": data_limite_str,
            "link": clean_parts[-1]
        }

        clean_data.append(mapper)    
    return clean_data

def parse_date_for_sorting(date_str):
    last_date = date_str.split('a')[-1].strip()

    try:
        if len(last_date) <= 5: 
            return datetime.strptime(f"{last_date}/{date.today().year}", "%d/%m/%Y")
        return datetime.strptime(last_date, "%d/%m/%Y")
    except:
        return datetime.max
    
def get_clean_data(clean_parts: List) -> str:
    raw_date = " ".join(clean_parts[1:-1]).lower()
    
    if "suspenso" in raw_date:
        return "Suspenso"
    
    date_pattern = r"\d{2}/\d{2}(?:/\d{4})?"
    interval_match = re.search(f"({date_pattern})\\s+a\\s+({date_pattern})", raw_date)
    
    if interval_match:
        return interval_match.group(0)
    
    dates_found = re.findall(date_pattern, raw_date)
    if dates_found:
        return dates_found[-1]

    return "A definir"


async def get_contest() -> List[Dict]:
    async with async_playwright() as p:
        try:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto(url)
            elements = await page.locator("div .da, .ea, .na").all()
            
            contest_data = []
            for el in elements:
                text = await el.inner_text()
                link = await el.get_attribute("data-url")
                contest_data.append(f"{text}\n{link}")
            
            data = clean_contest(contest_data)
            
            ordered_data = sorted(data, key=lambda x: parse_date_for_sorting(x['data_limite']))
            return ordered_data

        except Exception as e:
            print(e)
        finally:
                await browser.close()


        
