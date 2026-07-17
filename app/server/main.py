from routes.contests_routes import route as contests_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.config.config import setting

app = FastAPI()

app.include_router(contests_routes, prefix="/api/contests", tags=["Contests"])

origins = [o.strip() for o in setting.cors_url.split(",")]

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
