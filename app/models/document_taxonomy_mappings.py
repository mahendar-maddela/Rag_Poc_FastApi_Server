import uuid
import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    DECIMAL,
    ForeignKey,
    Enum,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base





class DocumentTaxonomyMapping(Base):
    __tablename__ = "document_taxonomy_mappings"
    __table_args__ = (
        UniqueConstraint("document_id", "taxonomy_id", name="uix_document_taxonomy"),
        {"schema": "rag_dev_ml"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    taxonomy_id = Column(UUID(as_uuid=True), ForeignKey("taxonomy_levels.id"), nullable=False)
    relevance_score = Column(DECIMAL(3, 2))  # 0.00–1.00
    classification_method = Column(String(20))
    classification_confidence = Column(DECIMAL(3, 2))
    classified_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    classified_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    verified = Column(Boolean, default=False)
    verified_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(TIMESTAMP(timezone=True))
    notes = Column(Text)

    # Relationships
    document = relationship("Document", backref="taxonomy_mappings")
    taxonomy = relationship("TaxonomyLevel", backref="document_mappings")
    classified_by = relationship("User", foreign_keys=[classified_by_user_id], backref="classified_documents")
    verified_by = relationship("User", foreign_keys=[verified_by_user_id], backref="verified_classifications")

