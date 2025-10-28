import uuid
import enum
from sqlalchemy import (
    Column,
    DECIMAL,
    Integer,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


# ENUM for tagging_method (shared meaning across tagging tables)
class TaggingMethod(enum.Enum):
    manual = "manual"
    auto_extraction = "auto_extraction"
    llm_generated = "llm_generated"


class ChunkKeyword(Base):
    __tablename__ = "chunk_keywords"
    # __table_args__ = (
    #     UniqueConstraint("chunk_id", "keyword_id", name="uix_chunk_keyword"),
    # )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id"), nullable=False)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=False)
    relevance_score = Column(DECIMAL(3, 2))
    mention_count = Column(Integer, default=0)
    tagging_method = Column(Enum(TaggingMethod, name="chunk_tagging_method_enum"))
    extraction_confidence = Column(DECIMAL(3, 2))
    tagged_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    chunk = relationship("DocumentChunk", backref="chunk_keywords")
    keyword = relationship("Keyword", backref="chunk_keywords")

