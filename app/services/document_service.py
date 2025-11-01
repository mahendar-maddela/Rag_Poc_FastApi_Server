import uuid
import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.core.s3_client import S3Client
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import DocumentCreateSchema
from app.models.user import User


class DocumentService:
    @staticmethod
    def upload_document(db: Session, file: UploadFile, data: DocumentCreateSchema, user: User):
        """Upload a document to Supabase S3 and store metadata in DB."""
        s3_client = S3Client()
        bucket = s3_client.bucket

        try:
            # Generate unique S3 path
            file_ext = file.filename.split(".")[-1]
            file_path = f"uploads/{uuid.uuid4()}-{file.filename}"
            content_type = file.content_type or "application/octet-stream"

            # Upload file to Supabase S3
            s3_client.upload_fileobj(file.file, bucket, file_path, content_type=content_type)

            # Generate signed URL
            signed_url = s3_client.generate_presigned_url(bucket_name=bucket, object_key=file_path)

            # Save document record
            document_data = {
                "title": data.title,
                "original_filename": file.filename,
                "file_type": file.content_type,
                "language_code": data.language,
                "visibility": data.visibility,
                "created_by_user_id": user.id,
                "file_size_bytes": getattr(file, "size", None),
                "file_hash": getattr(file, "hash", None),
            }
            document = DocumentRepository.create_document(db, document_data)

            # Save upload metadata
            upload_data = {
                "document_id": document.id,
                "uploaded_by_user_id": user.id,
                "cloud_storage_provider": "supabase-s3",
                "cloud_storage_bucket": bucket,
                "cloud_storage_path": file_path,
                "cloud_storage_url": signed_url,
                "upload_method": "api",
            }
            DocumentRepository.create_upload_entry(db, upload_data)

            db.commit()

            return {
                "message": "File uploaded successfully",
                "document_id": str(document.id),
                "file_url": signed_url,
            }

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    @staticmethod
    def get_all_documents(db: Session):
        """Fetch all documents with fresh presigned URLs."""
        s3_client = S3Client()
        bucket = s3_client.bucket

        rows = DocumentRepository.get_all_documents(db)
        documents = []

        for row in rows:
            signed_url = None
            if row.cloud_storage_path:
                try:
                    signed_url = s3_client.generate_presigned_url(bucket, row.cloud_storage_path)
                except Exception as e:
                    print(f"Error generating signed URL: {e}")

            documents.append({
                "document_id": str(row.document_id),
                "title": row.title,
                "original_filename": row.original_filename,
                "file_type": row.file_type,
                "document_created_at": row.document_created_at.isoformat() if row.document_created_at else None,
                "upload": {
                    "upload_id": str(row.upload_id),
                    "cloud_storage_url": signed_url,
                    "cloud_storage_path": row.cloud_storage_path,
                    "upload_created_at": row.upload_created_at.isoformat() if row.upload_created_at else None,
                },
            })

        return documents

    @staticmethod
    def get_file_metadata(db: Session, file_id: str):
        """Fetch metadata and fresh presigned URL for a single file."""
        document = DocumentRepository.get_document_with_upload(db, file_id)
        if not document:
            raise HTTPException(status_code=404, detail="File not found")

        upload = document.uploads[0] if document.uploads else None
        if not upload:
            raise HTTPException(status_code=400, detail="Upload data missing")

        s3_client = S3Client()
        signed_url = s3_client.generate_presigned_url(
            bucket_name=upload.cloud_storage_bucket,
            object_key=upload.cloud_storage_path,
        )

        return {
            "document_id": str(document.id),
            "title": document.title,
            "original_filename": document.original_filename,
            "file_type": document.file_type,
            "created_at": document.created_at.isoformat() if document.created_at else None,
            "file_url": signed_url,
        }
