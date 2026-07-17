from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional
import os

load_dotenv()


class __Settings(BaseSettings):

    database_url: str = os.getenv("DATABASE_URL") or "postgresql+psycopg://postgres:postgres@localhost:5432/concursos"

    redis_url: str = os.getenv("REDIS_URL") or "redis://localhost:6379/0"

    cors_url: str = os.getenv("CORS_URL") or "*"

    s3_endpoint: Optional[str] = os.getenv("S3_ENDPOINT")
    s3_region: str = os.getenv("S3_REGION") or "us-west-1"
    s3_acess_key: Optional[str] = os.getenv("S3_ACCESS_KEY")
    s3_secret_key: Optional[str] = os.getenv("S3_SECRET_KEY")
    s3_bucket: str = os.getenv("S3_BUCKET") or "editais-bot-concurso"

    class Config:
        env_file = ".env"
        extra = "ignore"

setting = __Settings()