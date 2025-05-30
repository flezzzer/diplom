from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class SellerCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    password: str

    class Config:
        orm_mode = True

class SellerLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class SellerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True

class SellerOut(SellerCreate):
    id: uuid.UUID

    class Config:
        orm_mode = True
