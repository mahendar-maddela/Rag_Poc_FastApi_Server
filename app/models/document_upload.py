import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    func,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class DocumentUpload(Base):
    __tablename__ = "document_uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    uploaded_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cloud_storage_provider = Column(String(50))  # e.g., s3, gcs, azure
    cloud_storage_bucket = Column(String(255))
    cloud_storage_path = Column(Text, nullable=False)
    cloud_storage_url = Column(Text)
    upload_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    upload_method = Column(String(50))  # e.g., ui, api, bulk_import
    upload_metadata = Column(JSON)  # stores IP, user-agent, etc.
    storage_verified_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    document = relationship("Document", backref="uploads")
    uploaded_by = relationship("User", backref="uploads")
