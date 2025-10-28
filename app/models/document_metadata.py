import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    DECIMAL,
    ForeignKey,
    Enum,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


# Define Enum types
from enum import Enum as PyEnum


class ExtractionSource(PyEnum):
    FILE_PROPERTIES = "file_properties"
    PARSED_CONTENT = "parsed_content"
    MANUAL = "manual"
    ENRICHED = "enriched"


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    metadata_key = Column(String(100), nullable=False)  # e.g., author, year, title
    metadata_value = Column(Text)
    metadata_value_normalized = Column(Text)
    extraction_source = Column(Enum(ExtractionSource, name="extraction_source"), nullable=False)
    confidence_score = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    extracted_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    verified_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(TIMESTAMP(timezone=True))

    # Relationships
    document = relationship("Document", backref="metadata_entries")
    verified_by = relationship("User", backref="verified_metadata")
