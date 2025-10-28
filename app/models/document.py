import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    BigInteger,
    Enum,
    TIMESTAMP,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

# Define enums for status and visibility
class DocumentStatus(enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    ready = "ready"
    failed = "failed"
    archived = "archived"


class DocumentVisibility(enum.Enum):
    public = "public"
    private = "private"
    restricted = "restricted"


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    original_filename = Column(Text, nullable=False)
    file_type = Column(String(50))
    file_size_bytes = Column(BigInteger)
    file_hash = Column(String(64))
    language_code = Column(String(10))
    current_status = Column(Enum(DocumentStatus, name="document_status_enum"), default=DocumentStatus.uploaded)
    visibility = Column(Enum(DocumentVisibility, name="document_visibility_enum"), default=DocumentVisibility.private)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))

    # Relationship with User model
    created_by = relationship("User", backref="documents")
