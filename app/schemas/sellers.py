from pydantic import BaseModel, EmailStr
from typing import Optional

# Схема для создания нового продавца
class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True

# Схема для обновления данных продавца
class SellerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True

# Схема для отображения информации о продавце
class SellerOut(SellerCreate):
    id: int

    class Config:
        orm_mode = True
