from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    status: OrderStatus
    total_amount: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    status: Optional[OrderStatus] = None

class OrderInDB(OrderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderOut(OrderInDB):
    pass
