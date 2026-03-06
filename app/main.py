from modules.workers.scheduler_contest import job_contests

from routes.contests_routes import route as contests_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import logging

load_dotenv()

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_contests, trigger="cron", hour=8, minute=0)
    scheduler.start()
    print("Agendador iniciado...")
    yield
    
    scheduler.shutdown()
    print("Agendador encerrado...")
    
app = FastAPI(lifespan=lifespan)

app.include_router(contests_routes, prefix="/api/contests", tags=["Contests"])

# origins = str(os.getenv("API_URL"))
origins = "http://localhost:5173/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healt():
    return {"status":"ok"}


