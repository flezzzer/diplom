from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryDelete(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryInDB(CategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryOut(CategoryInDB):
    pass
