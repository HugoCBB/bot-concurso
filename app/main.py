import asyncio
import json
from modules.scraping.extraction import get_contest
from modules.scraping.transform  import toJson
from modules.utils.file_dirs import FILE_JSON_DIR
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate

FILE_JSON = FILE_JSON_DIR / "data.json"

app = FastAPI()

@app.get("/")
async def healt():
    return {"status":"ok"}

@app.get("/api/contests/", response_model=Page[dict])
async def get_all_contest():
    with open(FILE_JSON, "r", encoding='utf-8') as file:
        data = json.load(file)
    return paginate(data)
add_pagination(app)


async def run():
    contest = await get_contest()
    toJson(contest)

if __name__ == "__main__":
    asyncio.run(run())