from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    category_id: UUID  # Используем UUID для category_id

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[UUID] = None  # Используем UUID для category_id

class ProductInDB(ProductBase):
    id: UUID  # Используем UUID для id
    created_at: datetime

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями

class ProductOut(ProductInDB):
    pass
