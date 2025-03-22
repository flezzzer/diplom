import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from clickhouse_sqlalchemy import engines
from app.db.session import Base
from app.db.session import get_db
from sqlalchemy.orm import relationship

# 🚀 Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    cart_items = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🏷 Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)

    products = relationship("Product", back_populates="category")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📦 Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category_id = Column(String, ForeignKey("categories.id"))
    seller_id = Column(String, ForeignKey("sellers.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    category = relationship("Category", back_populates="products")
    seller = relationship("Seller", back_populates="products")
    cart_items = relationship("Cart", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📋 Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    seller_id = Column(String, ForeignKey("sellers.id"))
    total_price = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="orders")
    seller = relationship("Seller", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🛒 Модель корзины
class Cart(Base):
    __tablename__ = "carts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Float, default=1)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# ⭐ Модель отзыва
class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    rating = Column(Float)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🏢 Модель продавца
class Seller(Base):
    __tablename__ = "sellers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String)
    password = Column(String)
    name = Column(String)
    email = Column(String)

    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="seller")

    __table_args__ = (
        engines.MergeTree(order_by=("id",), primary_key=("id",)),
    )

# 📦 Модель позиции заказа (для связи продуктов с заказами)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Float)
    price = Column(Float)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (engines.MergeTree(order_by="id"),)
