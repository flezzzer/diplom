from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.db.crud.category import create_category, get_category, get_categories, update_category, delete_category
from app.db.session import get_db
from app.core.auth import get_current_seller

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryCreate)
def create_new_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    if not current_seller:
        raise HTTPException(status_code=403, detail="Not authorized")
    return create_category(db, category, seller_id=current_seller.id)

@router.get("/{category_id}", response_model=CategoryCreate)
def read_category(category_id: str, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=list[CategoryCreate])
def read_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@router.put("/{category_id}")
def update_category_info(
    category_id: str,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    updated_category = update_category(db, category_id, category, seller_id=current_seller.id)
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found or not owned by the current seller")
    return updated_category

@router.delete("/{category_id}")
def delete_category_by_id(
    category_id: str,
    db: Session = Depends(get_db),
    current_seller = Depends(get_current_seller)
):
    deleted_category = delete_category(db, category_id, seller_id=current_seller.id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="Category not found or not owned by the current seller")
    return {"message": "Category successfully deleted"}
