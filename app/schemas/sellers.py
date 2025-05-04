from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# Схема для создания нового продавца
class SellerCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    password: str

    class Config:
        orm_mode = True

# Схема для логина продавца
class SellerLogin(BaseModel):
    email: EmailStr
    password: str

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
    id: uuid.UUID  # UUID заменяем на тип uuid.UUID для точности

    class Config:
        orm_mode = True
