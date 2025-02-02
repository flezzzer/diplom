from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

class ProductInDB(ProductBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями

class ProductOut(ProductInDB):
    pass
