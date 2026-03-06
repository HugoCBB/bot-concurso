from modules.utils.file_dirs import FILE_JSON_DIR
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter

import json


FILE_JSON = FILE_JSON_DIR / "data.json"
route = APIRouter()

@route.get("/", response_model=Page[dict])
async def get_all_contest():
    with open(FILE_JSON, "r", encoding='utf-8') as file:
        data = json.load(file)
    return paginate(data)
add_pagination(route)

