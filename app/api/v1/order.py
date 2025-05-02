from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.orders import OrderCreate, OrderOut
from app.db.crud.order import create_order_from_cart, get_order_by_id, get_orders_by_user, update_order_status, delete_order
from app.db.session import get_db
from app.core.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return  create_order_from_cart(db, user_id=current_user.id, order_data=order)

@router.get("/{order_id}", response_model=OrderCreate)
def read_order(order_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=list[OrderCreate])
def read_user_orders(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_orders_by_user(db, current_user.id)

@router.put("/{order_id}")
def update_status(order_id: str, status: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return update_order_status(db, order_id, status)

@router.delete("/{order_id}")
def delete_order_by_id(order_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_order(db, order_id)
