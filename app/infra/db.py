import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from modules.config.config import setting

logger = logging.getLogger(__name__)

DATABASE_URL = setting.database_url


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Cria as tabelas se nao existirem (substituir por Alembic em producao)."""
    from modules.models import contest

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tabelas verificadas/criadas no Postgres.")
