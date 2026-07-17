from typing import List, Dict
import json
import hashlib
from datetime import datetime
from datetime import date
import re
from modules.utils.file_dirs import FILE_JSON_DIR


FILE_JSON_NAME = FILE_JSON_DIR / "data.json"

def toJson(data: List[Dict]):
    try:
        with open(FILE_JSON_NAME, "w", encoding='utf-8') as j:
            json.dump(data, j, indent=4, ensure_ascii=False)
        print(f"Arquivo criado em {FILE_JSON_NAME}")
    except Exception as e:
        print(e)


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

        orgao = clean_parts[0]
        link = clean_parts[-1]

        mapper = {
            "fingerprint": make_fingerprint(orgao, link, data_limite_str),
            "orgao": orgao,
            "info": info,
            "cargo": cargo,
            "nivel": nivel,
            "data_limite": data_limite_str,
            "link": link
        }

        clean_data.append(mapper)
    return dedupe(clean_data)


def make_fingerprint(orgao: str, link: str, data_limite: str) -> str:
    """Identificador estavel de um concurso (base para dedupe/idempotencia)."""
    raw = f"{orgao.strip().lower()}|{link.strip().lower()}|{data_limite.strip().lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def dedupe(contests: List[Dict]) -> List[Dict]:
    """Remove concursos repetidos pelo fingerprint, preservando a ordem."""
    seen = set()
    unique = []
    for c in contests:
        fp = c["fingerprint"]
        if fp in seen:
            continue
        seen.add(fp)
        unique.append(c)
    return unique

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
