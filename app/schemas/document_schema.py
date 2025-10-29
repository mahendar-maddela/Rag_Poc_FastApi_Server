from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class DocumentCreateSchema(BaseModel):
    title: str
    language: str
    visibility: str  # public | private | restricted
    taxonomyId: Optional[UUID]

class DocumentResponseSchema(BaseModel):
    message: str
    document_id: str
    file_url: str
