from mongoengine import connect
from minio import Minio
from typing import List

class MongoDB():
    def __init__(self, mongo_dsn):
        connect(host=mongo_dsn)

class MinioClient():
    def __init__(self, endpoint, access_key, secret_key, secure = False):
        self.client = Minio(endpoint, access_key, secret_key, secure=secure)
        self.bucket: str


    def get_client(self) -> Minio:
        return self.client
    
    def get_bucket(self) -> str:
        return self.bucket
    
    def init_bucket(self, bucket_name:str):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.bucket = bucket_name
            