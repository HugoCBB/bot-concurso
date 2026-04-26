from modules.utils.file_dirs import FILE_JSON_DIR
from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter
from infra.redis_client import get_contests

route = APIRouter()

@route.get("/", response_model=Page[dict])
async def get_all_contest():
    data = await get_contests()
    return paginate(data)
add_pagination(route)

