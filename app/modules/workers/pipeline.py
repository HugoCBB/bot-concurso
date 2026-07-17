import asyncio
import logging
from datetime import datetime

from modules.scraping.extraction import get_contest, process_contest, delete_from_s3
from modules.repository.contest_repository import (
    upsert_contest,
    get_all_contests,
    get_expired_contests,
    delete_contests,
)
from infra.redis_client import save_contests
from playwright.async_api import async_playwright, Browser

logger = logging.getLogger(__name__)

WORKER_COUNT = 5           
MAX_CONCURRENT_PAGES = 5   


async def consumer(queue: asyncio.Queue, browser: Browser, sem: asyncio.Semaphore, results: list):
    while True:
        contest = await queue.get()
        try:
            if contest is None:
                break
            logger.info("Processing: %s", contest["orgao"])
            processed = await process_contest(contest, browser, sem)
            if processed is not None:
                await upsert_contest(processed)
                results.append(processed)
        finally:
            queue.task_done()


async def cleanup_expired() -> int:
    """Remove contests past their deadline: delete their PDFs from S3, then the DB rows.

    Keeps storage from growing without bound. Runs at the start of each job.
    """
    expired = await get_expired_contests(datetime.now())
    if not expired:
        return 0

    for contest in expired:
        for url in contest["edital_urls"]:
            try:
                await delete_from_s3(url)
            except Exception as e:
                logger.error("Failed to delete S3 object %s: %s", url, e)

    deleted = await delete_contests([c["id"] for c in expired])
    logger.info("Cleanup: removed %d expired contests (freed their editais).", deleted)
    return deleted


async def run_scraping() -> int:
    """Full scraping pipeline: scrape -> persist to Postgres -> refresh Redis cache.

    Reusable by both the standalone CLI (run_job.py) and the arq task.
    Returns the number of contests processed.
    """
    queue: asyncio.Queue = asyncio.Queue()
    sem = asyncio.Semaphore(MAX_CONCURRENT_PAGES)
    results: list = []

    # free storage first: drop contests past their deadline (DB + S3)
    await cleanup_expired()

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()

        workers = [
            consumer(queue, browser, sem, results)
            for _ in range(WORKER_COUNT)
        ]

        await asyncio.gather(
            get_contest(page, queue, worker_count=WORKER_COUNT),
            *workers,
        )

        await browser.close()

    await save_contests(await get_all_contests())
    logger.info("Job finished: %d contests processed", len(results))
    return len(results)
