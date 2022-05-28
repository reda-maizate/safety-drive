import os
from dataclasses import dataclass
import boto3

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = "safety-drive-bucket"


@dataclass
class S3:
    def __init__(self):
        self._client = self._connected_client()

    @staticmethod
    def _connected_client():
        """
        Connect to S3
        """
        return boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def upload_file(self, file_path, key):
        """
        Upload file to S3
        """
        self._client.upload_file(file_path, S3_BUCKET_NAME, key)
