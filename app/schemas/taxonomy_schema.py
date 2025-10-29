from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TaxonomyBase(BaseModel):
    level_number: int
    level_name: Optional[str]
    code: str
    display_name: str
    description: Optional[str]
    parent_id: Optional[UUID]
    path: Optional[str]
    level_order: Optional[int]
    icon_name: Optional[str]
    color_code: Optional[str]
    is_active: Optional[bool] = True

class TaxonomyCreate(TaxonomyBase):
    pass

class TaxonomyUpdate(BaseModel):
    level_name: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    parent_id: Optional[UUID]
    path: Optional[str]
    level_order: Optional[int]
    icon_name: Optional[str]
    color_code: Optional[str]
    is_active: Optional[bool]

class TaxonomyResponse(TaxonomyBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    created_by_user_id: UUID

    class Config:
        orm_mode = True
