import uuid
import enum
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import Base


# Define Role Enum
class UserRole(enum.Enum):
    admin = "admin"
    curator = "curator"
    contributor = "contributor"
    viewer = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(
        Enum(UserRole, name="user_role_enum"), nullable=False, default=UserRole.viewer
    )
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
