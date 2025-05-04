from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CartBase(BaseModel):
    pass  # Больше ничего здесь не нужно

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass  # Можно расширить, если будет нужно

class CartInDB(BaseModel):
    id: UUID  # Используем UUID вместо строки
    user_id: UUID  # Используем UUID для user_id
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CartOut(CartInDB):
    pass
