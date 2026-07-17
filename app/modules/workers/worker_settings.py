import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from arq import cron

from infra.arq_client import redis_settings
from modules.workers.pipeline import run_scraping

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def scrape_contests(ctx: dict) -> int:
    """arq task: run the full scraping pipeline. Also triggered on demand via the API."""
    logger.info("Starting scrape_contests (job %s)", ctx.get("job_id"))
    count = await run_scraping()
    logger.info("scrape_contests done: %d contests", count)
    return count


class WorkerSettings:
    """arq worker entrypoint: `arq modules.workers.worker_settings.WorkerSettings`."""

    functions = [scrape_contests]
    redis_settings = redis_settings
    cron_jobs = [
        cron(scrape_contests, hour={0, 6, 12, 18}, minute=0),
    ]
    max_jobs = 1          
    job_timeout = 60 * 30 
