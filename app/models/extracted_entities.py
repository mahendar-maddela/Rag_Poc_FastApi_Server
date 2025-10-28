import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    DECIMAL,
    Integer,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class ExtractedEntity(Base):
    __tablename__ = "extracted_entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="CASCADE"))
    entity_type = Column(String(50))  # e.g., PERSON, ORG, DATE, LOCATION, CONCEPT
    entity_text = Column(Text, nullable=False)
    entity_normalized = Column(Text)  # canonical form
    start_offset = Column(Integer)
    end_offset = Column(Integer)
    confidence_score = Column(DECIMAL(3, 2))
    extraction_method = Column(String(50))  # e.g., ner_model, rule_based, llm
    extracted_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    document = relationship("Document", backref="entities")
    chunk = relationship("DocumentChunk", backref="entities")
