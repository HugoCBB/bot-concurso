from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FOLDER_DATA = BASE_DIR / "datas"
FILE_PDF_DIR = FOLDER_DATA / "pdf"
FILE_JSON_DIR = FOLDER_DATA / "json"

FOLDER_DATA.mkdir(parents=True, exist_ok=True)
FILE_PDF_DIR.mkdir(parents=True, exist_ok=True)
FILE_JSON_DIR.mkdir(parents=True, exist_ok=True)



