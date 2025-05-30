from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.PENDING
    total_amount: Optional[float] = None

class OrderCreate(BaseModel):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderInDB(OrderBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderOut(OrderInDB):
    pass

class OrderStatusUpdate(BaseModel):
    order_id: UUID
    status: OrderStatus
    message: str
