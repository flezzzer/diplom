# app/api/v1/categories.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryDelete
from app.db.crud.category import create_category, get_category, get_categories, update_category, delete_category
from app.db.session import get_db
from app.core.auth import get_current_seller  # Получаем текущего продавца

router = APIRouter(prefix="/categories", tags=["Categories"])

# Создать категорию
@router.post("/", response_model=CategoryCreate)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)  # Получаем текущего продавца
):
    # Привязка категории к продавцу через current_seller
    return create_category(db, category, seller_id=current_seller.id)

# Получить категорию по ID
@router.get("/{category_id}", response_model=CategoryCreate)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Получить все категории
@router.get("/", response_model=list[CategoryCreate])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)

# Обновить категорию
@router.put("/{category_id}")
def update_category_info(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)  # Получаем текущего продавца
):
    # Привязка категории к продавцу через current_seller
    updated_category = update_category(db, category_id, category, seller_id=current_seller.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found or not owned by the current seller")
    return updated_category

# Удалить категорию
@router.delete("/{category_id}")
def delete_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)  # Получаем текущего продавца
):
    # Привязка категории к продавцу через current_seller
    deleted_category = delete_category(db, category_id, seller_id=current_seller.id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found or not owned by the current seller")
    return {"message": "Category successfully deleted"}
