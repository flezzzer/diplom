from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderBase(BaseModel):
    status: Optional[OrderStatus] = OrderStatus.PENDING
    total_amount: Optional[float] = None  # Вычисляется на основе корзины

class OrderCreate(BaseModel):
    # Поля явно от пользователя не требуются
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderInDB(OrderBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderOut(OrderInDB):
    pass

class OrderStatusUpdate(BaseModel):
    order_id: str
    status: OrderStatus
    message: str
