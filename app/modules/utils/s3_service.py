import boto3
from botocore.exceptions import ClientError

class S3Service:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def uploadToS3(self, file_path, file_name=None):
        if file_name is None:
            file_name = file_path
        
        try:
            self.s3.upload_file(file_path, self.bucket_name, file_name)
            print(f"Upload do arquivo {file_path} realizado com sucesso")

        except ClientError as e:
            print(f"Erro no upload:\n{e}")