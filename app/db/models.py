import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer
from clickhouse_sqlalchemy import engines
from app.db.session import Base
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
    description = Column(String)  # Поле description добавлено
    seller_id = Column(String, ForeignKey("sellers.id"))
    products = relationship("Product", back_populates="category")

    __table_args__ = (engines.MergeTree(order_by="id"),)


# 📦 Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    description = Column(String)  # Поле description добавлено
    price = Column(Float)
    category_id = Column(String, ForeignKey("categories.id"))
    seller_id = Column(String, ForeignKey("sellers.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    category = relationship("Category", back_populates="products")
    seller = relationship("Seller", back_populates="products")
    # cart_items = relationship("Cart", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    cart_products = relationship("CartProduct", back_populates="product")

    __table_args__ = (engines.MergeTree(order_by="id"),)


# 📋 Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    seller_id = Column(String, ForeignKey("sellers.id"))
    total_price = Column(Float)  # Переименовано в total_amount
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
    user = relationship("User", back_populates="cart_items")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связь с товарами через промежуточную таблицу CartProduct
    products = relationship("CartProduct", back_populates="cart")


# ⭐ Модель отзыва
class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    rating = Column(Float)
    review_text = Column(String)  # Поле review_text добавлено
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
    phone = Column(String, nullable=True)  # Добавлено поле phone
    address = Column(String, nullable=True)  # Добавлено поле address

    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="seller")

    __table_args__ = (
        engines.MergeTree(order_by="id"),
    )


# 📦 Модель позиции заказа (для связи продуктов с заказами)
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Float)
    price = Column(Float)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    __table_args__ = (engines.MergeTree(order_by="id"),)


class CartProduct(Base):
    __tablename__ = "cart_products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cart_id = Column(String, ForeignKey("carts.id"))
    product_id = Column(String, ForeignKey("products.id"))
    quantity = Column(Float, default=1)
    price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="products")
    product = relationship("Product", back_populates="cart_products")