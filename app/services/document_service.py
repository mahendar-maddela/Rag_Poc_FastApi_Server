import uuid
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.s3_client import s3_client
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import DocumentCreateSchema
from app.models.user import User
import os


class DocumentService:
    @staticmethod
    def upload_document(
        db: Session, file: UploadFile, data: DocumentCreateSchema, user: User
    ):
        try:
            bucket = os.getenv("SUPABASE_BUCKET")
            file_ext = file.filename.split(".")[-1]
            file_path = f"{user.id}/{uuid.uuid4()}.{file_ext}"

            # --- Upload to Supabase S3 ---
            s3_client.upload_fileobj(file.file, bucket, file_path)

            # Generate signed URL valid for 1 hour
            signed_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": file_path},
                ExpiresIn=3600,
            )

            # --- Save document record ---
            document_data = {
                "title": data.title,
                "original_filename": file.filename,
                "file_type": file.content_type,
                "language_code": data.language,
                "visibility": data.visibility,
                "created_by_user_id": user.id,
                "file_size_bytes": file.size,
                "file_hash": file.hash,
            }
            document = DocumentRepository.create_document(db, document_data)

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
            raise e

    @staticmethod
    def get_all_documents(db: Session):
        rows = DocumentRepository.get_all_documents(db)

        documents = []
        for row in rows:
            documents.append(
                {
                    "document_id": str(row.document_id),
                    "title": row.title,
                    "original_filename": row.original_filename,
                    "file_type": row.file_type,
                    "document_created_at": row.document_created_at.isoformat()
                    if row.document_created_at
                    else None,
                    "upload": {
                        "upload_id": str(row.upload_id),
                        "cloud_storage_url": row.cloud_storage_url,
                        "cloud_storage_path": row.cloud_storage_path,
                        "upload_created_at": row.upload_created_at.isoformat()
                        if row.upload_created_at
                        else None,
                    },
                }
            )

        return documents
