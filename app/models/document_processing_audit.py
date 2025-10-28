from sqlalchemy import Column, ForeignKey, Enum, JSON, Text, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
import enum
import uuid
from app.db.database import Base
from datetime import datetime


class ActionType(enum.Enum):
    created = "created"
    updated = "updated"
    reprocessed = "reprocessed"
    deleted = "deleted"
    restored = "restored"


class DocumentProcessingAudit(Base):
    __tablename__ = "document_processing_audit"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    action_type = Column(Enum(ActionType, name="action_type_enum"), nullable=False)
    action_timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    performed_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    performed_by_system = Column(String(100))
    changes_made = Column(JSON)
    reason = Column(Text)
    ip_address = Column(INET)

    document = relationship("Document", backref="audit_logs")
    user = relationship("User", backref="audit_actions")
