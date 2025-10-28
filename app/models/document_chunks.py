import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index = Column(Integer, nullable=False)  # sequential order
    chunk_text = Column(Text, nullable=False)
    chunk_text_tokens = Column(Integer)  # number of tokens for LLM context
    chunk_hash = Column(String(64))  # for deduplication/change detection
    chunk_type = Column(String(50))
    parent_chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id"))
    meta_data = Column("metadata", JSON)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    # Relationships
    document = relationship("Document", backref="chunks")
    parent_chunk = relationship("DocumentChunk", remote_side=[id], backref="sub_chunks")
