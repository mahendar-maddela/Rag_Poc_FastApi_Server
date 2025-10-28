import uuid
import enum
from sqlalchemy import (
    Column,
    DECIMAL,
    String,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    UniqueConstraint,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


# ENUM for tagging_method
class TaggingMethod(enum.Enum):
    manual = "manual"
    auto_extraction = "auto_extraction"
    llm_generated = "llm_generated"


class DocumentKeyword(Base):
    __tablename__ = "document_keywords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=False)
    relevance_score = Column(DECIMAL(3, 2))
    tagging_method = Column(Enum(TaggingMethod, name="tagging_method_enum"))
    extraction_confidence = Column(DECIMAL(3, 2))
    tagged_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    tagged_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    verified = Column(Boolean, default=False)
    verified_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    document = relationship("Document", backref="document_keywords")
    keyword = relationship("Keyword", backref="document_keywords")
    tagged_by = relationship("User", foreign_keys=[tagged_by_user_id], backref="tagged_keywords")
    verified_by = relationship("User", foreign_keys=[verified_by_user_id], backref="verified_keywords")
