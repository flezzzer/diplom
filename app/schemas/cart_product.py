from pydantic import BaseModel
from uuid import UUID
from typing import Optional

# cart_product.py

class CartProductCreate(BaseModel):
    product_id: UUID
    quantity: int

class CartProductBase(BaseModel):
    product_id: UUID
    cart_id: UUID
    quantity: int

class CartProductRead(CartProductBase):
    id: UUID

    class Config:
        orm_mode = True
