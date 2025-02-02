from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Для работы с SQLAlchemy моделями

class CategoryOut(UserInDB):
    pass


class UserLogOut(UserBase):
    pass


# Вход пользователя
class UserLogin(BaseModel):
    email: EmailStr
    password: str



