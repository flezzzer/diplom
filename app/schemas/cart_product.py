from pydantic import BaseModel
from typing import Optional
import uuid

# cart_product.py

class CartProductCreate(BaseModel):
    product_id: str
    quantity: int  # добавь, если нужно

class CartProductBase(BaseModel):
    product_id: str
    cart_id: str
    quantity: int

class CartProductRead(CartProductBase):
    id: str

    class Config:
        orm_mode = True

