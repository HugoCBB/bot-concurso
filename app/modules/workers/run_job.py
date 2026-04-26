import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.scraping.extraction import get_contest
from infra.redis_client import save_contests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

async def main():
    logger.info("Iniciando busca de concursos...")
    contests = await get_contest()

    if not contests:
        logger.warning("Nenhum concurso encontrado. Redis não atualizado.")
        return

    await save_contests(contests)
    logger.info("Job finalizado com sucesso!")
    
asyncio.run(main())

 
