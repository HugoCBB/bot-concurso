from routes.contests_routes import route as contests_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import os

load_dotenv()
    
app = FastAPI()

app.include_router(contests_routes, prefix="/api/contests", tags=["Contests"])

origins = str(os.getenv("CORS_URL"))

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
