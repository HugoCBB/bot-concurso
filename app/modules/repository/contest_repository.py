import logging
from datetime import datetime
from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db import async_session
from modules.models.contest import Contest, Edital
from modules.scraping.transform import parse_date_for_sorting

logger = logging.getLogger(__name__)

_CONTEST_FIELDS = ("orgao", "info", "cargo", "nivel", "data_limite", "link", "source")


async def _apply_contest(session: AsyncSession, data: Dict) -> bool:
    """Insert or update a single contest by fingerprint within an open session.

    Returns True if applied, False if skipped (no fingerprint).
    """
    fp = data.get("fingerprint")
    if not fp:
        logger.warning("Contest without fingerprint, skipped: %s", data.get("orgao"))
        return False

    result = await session.execute(select(Contest).where(Contest.fingerprint == fp))
    contest = result.scalar_one_or_none()

    if contest is None:
        contest = Contest(fingerprint=fp)
        session.add(contest)

    for field in _CONTEST_FIELDS:
        if field in data and data[field] is not None:
            setattr(contest, field, data[field])

    contest.editais = [
        Edital(s3_url=url) for url in data.get("edital_urls", []) if url
    ]
    return True


async def upsert_contest(data: Dict) -> bool:
    """Persist a single contest immediately (incremental save)."""
    async with async_session() as session:
        applied = await _apply_contest(session, data)
        if applied:
            await session.commit()
            logger.debug("Saved contest: %s", data.get("orgao"))
    return applied


async def upsert_contests(contests: List[Dict]) -> int:
    """Persist many contests in one transaction (batch save)."""
    saved = 0
    async with async_session() as session:
        for data in contests:
            if await _apply_contest(session, data):
                saved += 1
        await session.commit()
    logger.info("%d contests saved/updated in Postgres.", saved)
    return saved


async def get_expired_contests(now: datetime | None = None) -> List[Dict]:
    """Contests whose deadline (data_limite) is in the past.

    'Suspenso' / 'A definir' parse to datetime.max, so they are never expired.
    Returns dicts with id, orgao and the S3 URLs of their editais.
    """
    now = now or datetime.now()
    async with async_session() as session:
        result = await session.execute(select(Contest))
        contests = result.scalars().all()
        return [
            {
                "id": c.id,
                "orgao": c.orgao,
                "edital_urls": [e.s3_url for e in c.editais],
            }
            for c in contests
            if parse_date_for_sorting(c.data_limite) < now
        ]


async def delete_contests(ids: List[int]) -> int:
    """Delete contests by id (cascade removes their editais rows). Returns count."""
    if not ids:
        return 0
    async with async_session() as session:
        result = await session.execute(select(Contest).where(Contest.id.in_(ids)))
        contests = result.scalars().all()
        for contest in contests:
            await session.delete(contest)
        await session.commit()
    logger.info("%d expired contests deleted from Postgres.", len(contests))
    return len(contests)


async def get_all_contests() -> List[Dict]:
    """List all contests (with their editais) as dicts, ordered by deadline."""
    async with async_session() as session:
        result = await session.execute(select(Contest).order_by(Contest.data_limite))
        contests = result.scalars().all()

        return [
            {
                "id": c.id,
                "fingerprint": c.fingerprint,
                "source": c.source,
                "orgao": c.orgao,
                "info": c.info,
                "cargo": c.cargo,
                "nivel": c.nivel,
                "data_limite": c.data_limite,
                "link": c.link,
                "edital_urls": [e.s3_url for e in c.editais],
            }
            for c in contests
        ]
