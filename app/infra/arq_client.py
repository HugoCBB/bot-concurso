import os
from arq.connections import RedisSettings, create_pool
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_settings = RedisSettings.from_dsn(REDIS_URL)

_pool = None


async def get_arq_pool():
    """Lazily create a shared arq Redis pool (used by the API to enqueue jobs)."""
    global _pool
    if _pool is None:
        _pool = await create_pool(redis_settings)
    return _pool
