from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from clickhouse_sqlalchemy import engines
from app.db.session import Base
import datetime
from sqlalchemy.orm import relationship

# 🚀 Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с корзинами
    cart_items = relationship("Cart", back_populates="user")

    # Связь с заказами
    orders = relationship("Order", back_populates="user")

    # Связь с отзывами
    reviews = relationship("Review", back_populates="user")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🏷 Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    name = Column(String)

    # Связь с продуктами
    products = relationship("Product", back_populates="category")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📦 Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))  # Связь с категорией
    seller_id = Column(Integer, ForeignKey("sellers.id"))  # Связь с продавцом
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с категорией
    category = relationship("Category", back_populates="products")

    # Связь с продавцом
    seller = relationship("Seller", back_populates="products")

    # Связь с корзиной
    cart_items = relationship("Cart", back_populates="product")

    # Связь с отзывами
    reviews = relationship("Review", back_populates="product")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 📋 Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    seller_id = Column(Integer, ForeignKey("sellers.id"))  # Связь с продавцом
    total_price = Column(Float)
    status = Column(String, default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с пользователем
    user = relationship("User", back_populates="orders")

    # Связь с продавцом
    seller = relationship("Seller", back_populates="orders")

    # Связь с товарами в заказе
    order_items = relationship("OrderItem", back_populates="order")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🛒 Модель корзины
class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    product_id = Column(Integer, ForeignKey("products.id"))  # Связь с продуктом
    quantity = Column(Integer, default=1)

    # Связь с пользователем
    user = relationship("User", back_populates="cart_items")

    # Связь с продуктом
    product = relationship("Product", back_populates="cart_items")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# ⭐ Модель отзыва
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    product_id = Column(Integer, ForeignKey("products.id"))  # Связь с продуктом
    rating = Column(Integer)  # 1-5
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с пользователем
    user = relationship("User", back_populates="reviews")

    # Связь с продуктом
    product = relationship("Product", back_populates="reviews")

    __table_args__ = (engines.MergeTree(order_by="id"),)

# 🏢 Модель продавца
class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    email = Column(String)

    # Связь с продуктами
    products = relationship("Product", back_populates="seller")

    # Связь с заказами
    orders = relationship("Order", back_populates="seller")

    __table_args__ = (
        engines.MergeTree(
            order_by=('id',),  # Указываем поле для сортировки
            primary_key=('id',),  # Указываем первичный ключ
            index=[('name', 'index_name')]  # Пример добавления индекса
        ),
    )

# 📦 Модель позиции заказа (для связи продуктов с заказами)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ⬅ PRIMARY KEY
    order_id = Column(Integer, ForeignKey("orders.id"))  # Связь с заказом
    product_id = Column(Integer, ForeignKey("products.id"))  # Связь с продуктом
    quantity = Column(Integer)
    price = Column(Float)

    # Связь с заказом
    order = relationship("Order", back_populates="order_items")

    # Связь с продуктом
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (engines.MergeTree(order_by="id"),)
