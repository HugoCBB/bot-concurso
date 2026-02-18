from typing import List, Dict
import json
from modules.utils.file_dirs import FILE_JSON_DIR


FILE_JSON_NAME = FILE_JSON_DIR / "data.json"

def toJson(data: List[Dict]):
    try:
        with open(FILE_JSON_NAME, "w", encoding='utf-8') as j:
            json.dump(data, j, indent=4, ensure_ascii=False)
        print(f"Arquivo criado em {FILE_JSON_NAME}")
    except Exception as e:
        print(e)


    