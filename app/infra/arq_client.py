from arq.connections import RedisSettings, create_pool

from modules.config.config import setting

redis_settings = RedisSettings.from_dsn(setting.redis_url)

_pool = None


async def get_arq_pool():
    """Lazily create a shared arq Redis pool (used by the API to enqueue jobs)."""
    global _pool
    if _pool is None:
        _pool = await create_pool(redis_settings)
    return _pool
