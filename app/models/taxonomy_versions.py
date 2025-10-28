import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    Integer,
    ForeignKey,
    Enum,
    JSON,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class ChangeType(enum.Enum):
    created = "created"
    updated = "updated"
    moved = "moved"
    merged = "merged"
    split = "split"
    deactivated = "deactivated"


class TaxonomyVersion(Base):
    __tablename__ = "taxonomy_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    taxonomy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("taxonomy_levels.id", ondelete="CASCADE"),
        nullable=False,
    )
    version_number = Column(Integer, nullable=False)
    change_type = Column(Enum(ChangeType), nullable=False)
    previous_values = Column(JSON)
    new_values = Column(JSON)
    change_reason = Column(Text)
    changed_by_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
    )
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    affected_document_count = Column(Integer)
    migration_completed = Column(Boolean, default=False)

    # Relationships
    taxonomy = relationship("TaxonomyLevel", backref="versions")
    changed_by = relationship("User", backref="taxonomy_changes")
