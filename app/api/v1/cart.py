from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.cart import CartCreate, CartUpdate
from app.db.crud.cart import get_cart, add_product_to_cart, remove_product_from_cart, delete_cart
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartCreate)
def read_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_cart(db, current_user["id"])

@router.post("/")
def add_product_to_cart(cart_item: CartCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return add_product_to_cart(db, user_id=current_user["id"], cart_item=cart_item)

@router.delete("/{product_id}")
def remove_product_from_cart(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return remove_product_from_cart(db, user_id=current_user["id"], product_id=product_id)

@router.delete("/")
def clear_user_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_cart(db, user_id=current_user["id"])
