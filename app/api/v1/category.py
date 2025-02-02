from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryDelete
from app.db.crud.category import create_category, get_category, get_categories, update_category, delete_category
from app.db.session import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

# Создать категорию
@router.post("/", response_model=CategoryCreate)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

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
def update_category_info(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category(db, category_id, category)


@router.delete("/{category_id}", response_model=CategoryDelete)
def delete_category(category_id: int, category: CategoryDelete, db: Session = Depends(get_db)):
    return delete_category(category_id, category, db)

# Удалить категорию
