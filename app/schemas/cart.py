from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass

class CartInDB(BaseModel):
    id: UUID  # Используем UUID вместо строки
    user_id: UUID  # Используем UUID для user_id
    updated_at: datetime

    class Config:
        orm_mode = True

class CartOut(CartInDB):
    pass
