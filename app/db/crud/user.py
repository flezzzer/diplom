from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.users import UserRegister, UserUpdate
from app.security import hash_password, verify_password

# Создание пользователя
def create_user(db: Session, user: UserRegister):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return db_user

# Получение пользователя по id
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Получение пользователя по email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Получение всех пользователей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

# Обновление пользователя
def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.username:
            db_user.username = user.username
        if user.email:
            db_user.email = user.email
        if user.full_name:
            db_user.full_name = user.full_name
        if user.is_active is not None:
            db_user.is_active = user.is_active
        db.commit()
        db.refresh(db_user)
    return db_user

# Удаление пользователя
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
