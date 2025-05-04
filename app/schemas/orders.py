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
    total_amount: Optional[float] = None  # Вычисляется на основе корзины

class OrderCreate(BaseModel):
    # Поля явно от пользователя не требуются
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderInDB(OrderBase):
    id: UUID  # Используем UUID для id
    user_id: UUID  # Используем UUID для user_id
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderOut(OrderInDB):
    pass

class OrderStatusUpdate(BaseModel):
    order_id: UUID  # Используем UUID для order_id
    status: OrderStatus
    message: str
