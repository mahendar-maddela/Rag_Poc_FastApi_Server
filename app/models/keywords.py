import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    TIMESTAMP,
    Enum,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


# Enum for keyword status
class KeywordStatus(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    merged = "merged"


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword_type_id = Column(UUID(as_uuid=True), ForeignKey("keyword_types.id"), nullable=False)
    keyword_text = Column(String(255), nullable=False)
    keyword_normalized = Column(String(255), nullable=False)
    keyword_slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    usage_count = Column(Integer, default=0)
    status = Column(Enum(KeywordStatus), default=KeywordStatus.pending)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_at = Column(TIMESTAMP(timezone=True))
    merged_into_keyword_id = Column(UUID(as_uuid=True), ForeignKey("keywords.id"))

    # Relationships
    keyword_type = relationship("KeywordType", backref="keywords")
    created_by = relationship("User", foreign_keys=[created_by_user_id], backref="created_keywords")
    approved_by = relationship("User", foreign_keys=[approved_by_user_id], backref="approved_keywords")
    merged_into = relationship("Keyword", remote_side=[id], backref="merged_keywords")
