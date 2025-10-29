from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_upload import DocumentUpload
from sqlalchemy.orm import joinedload


class DocumentRepository:
    @staticmethod
    def create_document(db: Session, document_data: dict) -> Document:
        document = Document(**document_data)
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def create_upload_entry(db: Session, upload_data: dict) -> DocumentUpload:
        upload = DocumentUpload(**upload_data)
        db.add(upload)
        db.commit()
        db.refresh(upload)
        return upload

    @staticmethod
    def get_all_documents(db: Session):
        query = (
            db.query(
                Document.id.label("document_id"),
                Document.title,
                Document.original_filename,
                Document.file_type,
                Document.created_at.label("document_created_at"),
                DocumentUpload.id.label("upload_id"),
                DocumentUpload.cloud_storage_url,
                DocumentUpload.cloud_storage_path,
                DocumentUpload.created_at.label("upload_created_at"),
            )
            .join(DocumentUpload, Document.id == DocumentUpload.document_id)
            .order_by(Document.created_at.desc())
        )

        return query.all()
