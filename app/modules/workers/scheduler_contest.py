from modules.scraping.extraction import get_contest
from modules.scraping.transform import toJson

async def job_contests():
    contest = await get_contest()
    toJson(contest)