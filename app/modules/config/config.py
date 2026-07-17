from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class __Settings(BaseSettings):

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/concursos"

    redis_url: str = "redis://localhost:6379/0"

    cors_url: str = "*"

    s3_endpoint: Optional[str] = None
    s3_region: str = "us-west-1"
    s3_acess_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_bucket: str = "editais-bot-concurso"

    @field_validator("database_url", "redis_url", "cors_url", "s3_region", "s3_bucket", mode="before")
    @classmethod
    def _fallback_on_empty(cls, value, info):
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return cls.model_fields[info.field_name].default
        return value

    class Config:
        env_file = ".env"
        extra = "ignore"

setting = __Settings()