from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class __Settings(BaseSettings):
    
    s3_endpoint: str = os.getenv("S3_ENDPOINT")
    s3_region: str =  os.getenv('S3_REGION') or "us-west-1"
    s3_acess_key: str = os.getenv("S3_ACCESS_KEY")
    s3_secret_key: str = os.getenv("S3_SECRET_KEY")
    s3_bucket: str = os.getenv("S3_BUCKET") or "editais-bot-concurso"

    class Config:
        env_file = ".env"
        extra = "ignore"

setting = __Settings()