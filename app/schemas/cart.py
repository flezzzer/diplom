from pydantic import BaseModel
from datetime import datetime

class CartBase(BaseModel):
    pass  # Больше ничего здесь не нужно

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass  # Можно расширить, если будет нужно

class CartInDB(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CartOut(CartInDB):
    pass
