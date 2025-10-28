import uuid
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
    DECIMAL,
    Integer,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Index
from pgvector.sqlalchemy import Vector  # requires pgvector installed


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False, unique=True)
    embedding_model = Column(String(100))  # e.g., text-embedding-3-large
    embedding_version = Column(String(50))
    embedding_vector = Column(Vector(1536))  # pgvector column
    embedding_dimension = Column(Integer)
    generated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    generation_cost = Column(DECIMAL(10, 6))  # API cost tracking (e.g., OpenAI tokens)

    # Relationship
    chunk = relationship("DocumentChunk", backref="embedding")