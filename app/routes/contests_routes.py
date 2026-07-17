from fastapi_pagination import Page, add_pagination, paginate
from fastapi import APIRouter
from infra.redis_client import get_contests, save_contests
from infra.arq_client import get_arq_pool
from modules.repository.contest_repository import get_all_contests

route = APIRouter()


@route.get("/", response_model=Page[dict])
async def get_all_contest():
    data = await get_contests()
    if not data:
        data = await get_all_contests()
        if data:
            await save_contests(data)
    return paginate(data)


@route.post("/refresh", status_code=202)
async def trigger_refresh():
    """Enqueue a scraping run on the arq worker (non-blocking)."""
    pool = await get_arq_pool()
    job = await pool.enqueue_job("scrape_contests")
    return {"status": "enqueued", "job_id": job.job_id if job else None}


add_pagination(route)
