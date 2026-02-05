from typing import List, Dict
import json
import asyncio
from modules.utils.file_dirs import FILE_JSON_DIR
from modules.scraping.extraction import Extraction

FILE_JSON_NAME = FILE_JSON_DIR / "data.json"

def toJson(data: List[Dict]):
    try:
        with open(FILE_JSON_NAME, "w", encoding='utf-8') as j:
            json.dump(data, j, indent=4, ensure_ascii=False)
        print(f"Arquivo {FILE_JSON_NAME} criado com sucesso")
    except Exception as e:
        print(e)

data =  asyncio.run(Extraction.get_contest())
toJson(Extraction.clean_contest(data))

    