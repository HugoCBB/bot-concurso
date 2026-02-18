import asyncio
from modules.scraping.extraction import get_contest
from modules.scraping.transform  import toJson

async def run():
    contest = await get_contest()
    toJson(contest)

if __name__ == "__main__":
    asyncio.run(run())