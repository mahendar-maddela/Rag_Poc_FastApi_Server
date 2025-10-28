import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    Integer,
    ForeignKey,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class TaxonomyLevel(Base):
    __tablename__ = "taxonomy_levels"


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level_number = Column(Integer, nullable=False)  # e.g., 1, 2, 3, 4
    level_name = Column(String(100))  # e.g., Domain, Category, Topic
    code = Column(String(50), nullable=False, unique=True)  # e.g., GS-POL-GOV-FED
    display_name = Column(String(255), nullable=False)
    description = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("taxonomy_levels.id"))
    path = Column(Text)  # e.g., /1/5/23/
    level_order = Column(Integer)
    icon_name = Column(String(50))
    color_code = Column(String(7))  # e.g., #FF5733
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    # Relationships
    parent = relationship("TaxonomyLevel", remote_side=[id], backref="children")
    created_by = relationship("User", backref="created_taxonomies")
