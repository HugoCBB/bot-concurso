import redis.asyncio as rd
import json
import logging

from modules.config.config import setting

logger = logging.getLogger(__name__)
REDIS_URL = setting.redis_url
CONTEST_KEY = "contest:list"
CONTESTS_TTL = 60 * 60 * 25

_redis_client = None

async def get_redis():
    global _redis_client
    
    if _redis_client is None:
        _redis_client = rd.from_url(REDIS_URL, decode_responses=True)
    
    return _redis_client


async def save_contests(contests:list[dict]):
    r = await get_redis()
    await r.set(CONTEST_KEY, json.dumps(contests, ensure_ascii=False), ex=CONTESTS_TTL)
    logger.info(f"{len(contests)} concursos salvos no Redis.")
    
async def get_contests() -> list[dict]:
    r = await get_redis()
    data = await r.get(CONTEST_KEY)
    return json.loads(data) if data else []