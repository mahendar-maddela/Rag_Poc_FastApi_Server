import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    func,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class KeywordType(Base):
    __tablename__ = "keyword_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = Column(String(100), nullable=False, unique=True)  # e.g., topic, person, event
    type_description = Column(Text)
    type_color = Column(String(7))  # Hex color code for UI
    validation_regex = Column(Text)  # Optional regex for validation
    requires_approval = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    created_by = relationship("User", backref="created_keyword_types")
