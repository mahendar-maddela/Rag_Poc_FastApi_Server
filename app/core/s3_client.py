import os
import boto3

s3_client = boto3.client(
    "s3",
    region_name=os.getenv("SUPABASE_S3_REGION"),
    endpoint_url=os.getenv("SUPABASE_S3_ENDPOINT"),
    aws_access_key_id=os.getenv("SUPABASE_S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SUPABASE_S3_SECRET_KEY"),
)
