import boto3
from botocore.config import Config
from modules.config.config import setting

def get_s3_client() -> boto3.client:
    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=setting.s3_endpoint,
            region_name=setting.s3_region,
            aws_access_key_id=setting.s3_access_key,
            aws_secret_access_key=setting.s3_secret_key,
            config=Config(signature_version="s3v4"),
        )
        return s3
    except Exception as e:
        print(e)

