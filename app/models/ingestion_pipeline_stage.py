import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    func,
    Integer,
    JSON,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


# Define ENUM types for stage_name and stage_status
from enum import Enum as PyEnum


class StageName(PyEnum):
    uploaded = "uploaded"
    parsed = "parsed"
    chunked = "chunked"
    embedded = "embedded"
    indexed = "indexed"
    failed = "failed"


class StageStatus(PyEnum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class IngestionPipelineStage(Base):
    __tablename__ = "ingestion_pipeline_stages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    stage_name = Column(Enum(StageName, name="ingestion_stage_name"), nullable=False)
    stage_status = Column(Enum(StageStatus, name="ingestion_stage_status"), nullable=False, default=StageStatus.pending)
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True))
    duration_ms = Column(Integer)
    processing_node = Column(String(100))  # which worker handled it
    stage_output = Column(JSON)  # stores results, metrics
    error_message = Column(Text)
    error_stack_trace = Column(Text)
    retry_count = Column(Integer, default=0)
    triggered_by = Column(String(50))  # manual, automatic, reprocess

    # Relationship
    document = relationship("Document", backref="pipeline_stages")
