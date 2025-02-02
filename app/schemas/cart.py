from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class CartBase(BaseModel):
    total_amount: float

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    total_amount: Optional[float] = None

class CartInDB(CartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CartOut(CartInDB):
    pass
