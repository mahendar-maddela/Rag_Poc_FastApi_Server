import os
import boto3
from fastapi import HTTPException
from io import BytesIO


class S3Client:
    def __init__(self):
        """Initialize a boto3 S3 client with Supabase-compatible endpoint."""
        self.s3 = boto3.client(
            "s3",
            region_name=os.getenv("SUPABASE_S3_REGION"),
            endpoint_url=os.getenv("SUPABASE_S3_ENDPOINT"),
            aws_access_key_id=os.getenv("SUPABASE_S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("SUPABASE_S3_SECRET_KEY"),
        )
        self.bucket = os.getenv("SUPABASE_BUCKET")

    def upload_fileobj(
        self, file_obj, bucket_name: str, object_key: str, content_type: str = None
    ):
        """Uploads a file object to Supabase S3 bucket."""
        try:
            extra_args = {"ContentType": content_type} if content_type else {}
            self.s3.upload_fileobj(
                file_obj, bucket_name, object_key, ExtraArgs=extra_args
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

    def upload_bytes(
        self, data: bytes, object_key: str, content_type: str = "text/plain"
    ):
        """Uploads bytes directly to S3 (for text or generated files)."""
        try:
            self.s3.upload_fileobj(
                BytesIO(data),
                self.bucket,
                object_key,
                ExtraArgs={"ContentType": content_type},
            )
            return f"{self.bucket}/{object_key}"
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload bytes to S3: {str(e)}"
            )

    def generate_presigned_url(
        self, bucket_name: str, object_key: str, expires_in: int = 3600
    ):
        """Generate a temporary presigned URL (default 1 hour)."""
        try:
            return self.s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": bucket_name,
                    "Key": object_key,
                    "ResponseContentDisposition": "inline",  # 👈 display in browser
                },
                ExpiresIn=expires_in,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate presigned URL: {str(e)}"
            )
