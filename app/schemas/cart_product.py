from pydantic import BaseModel
from uuid import UUID
from typing import Optional

# cart_product.py

class CartProductCreate(BaseModel):
    product_id: UUID  # Используем UUID для product_id
    quantity: int  # добавь, если нужно

class CartProductBase(BaseModel):
    product_id: UUID  # Используем UUID для product_id
    cart_id: UUID  # Используем UUID для cart_id
    quantity: int

class CartProductRead(CartProductBase):
    id: UUID  # Используем UUID для id

    class Config:
        orm_mode = True
