import uuid
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class KeywordSynonym(Base):
    __tablename__ = "keyword_synonyms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"), nullable=False)
    synonym_text = Column(String(255), nullable=False)
    synonym_normalized = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    primary_keyword = relationship("Keyword", backref="synonyms")
    created_by = relationship("User", backref="created_synonyms")
