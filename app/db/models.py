from sqlalchemy import Column, Integer, String, DateTime, Float
from clickhouse_sqlalchemy import engines
from app.db.session import Base
import datetime

# 🚀 Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🏷 Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    name = Column(String)

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📦 Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📋 Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer)
    total_price = Column(Float)
    status = Column(String, default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🛒 Модель корзины
class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer, default=1)

    __table_args__ = (engines.MergeTree(order_by="id"),)

# ⭐ Модель отзыва
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer)
    product_id = Column(Integer)
    rating = Column(Integer)  # 1-5
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (engines.MergeTree(order_by="id"),)
