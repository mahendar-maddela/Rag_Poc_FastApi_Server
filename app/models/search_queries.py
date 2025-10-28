import uuid
import enum
from sqlalchemy import (
    Column,
    Text,
    Integer,
    TIMESTAMP,
    ForeignKey,
    JSON,
    Enum,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector  # requires pgvector installed
from app.db.database import Base


# ENUM for search type
class SearchType(enum.Enum):
    semantic = "semantic"
    keyword = "keyword"
    hybrid = "hybrid"


class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    query_text = Column(Text, nullable=False)
    query_embedding = Column(Vector(1536))  # pgvector field for semantic caching
    search_type = Column(Enum(SearchType, name="search_type_enum"))
    filters_applied = Column(JSON)
    results_count = Column(Integer)
    query_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    response_time_ms = Column(Integer)
    user_clicked_results = Column(ARRAY(Integer))  # array of chunk IDs clicked

    # Relationship
    user = relationship("User", backref="search_queries")
