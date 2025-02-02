from sqlalchemy.orm import Session
from app.db.models import Cart, Product
from app.schemas.cart import CartCreate, CartUpdate
from sqlalchemy.orm import aliased

# Создание корзины
def create_cart(db: Session, user_id: int, cart: CartCreate):
    db_cart = Cart(user_id=user_id, total_amount=cart.total_amount)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

# Получение корзины по user_id
def get_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()

# Обновление корзины
def update_cart(db: Session, cart_id: int, cart: CartUpdate):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if db_cart:
        if cart.total_amount is not None:
            db_cart.total_amount = cart.total_amount
        db.commit()
        db.refresh(db_cart)
    return db_cart

# Удаление корзины
def delete_cart(db: Session, cart_id: int):
    db_cart = db.query(Cart).filter(Cart.id == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
    return db_cart

# Добавление товара в корзину (привязываем товар к корзине через вспомогательную таблицу)
def add_product_to_cart(db: Session, cart_id: int, product_id: int, quantity: int, price: float):
    cart_product = db.query(cart_product).filter(
        cart_product.c.cart_id == cart_id,
        cart_product.c.product_id == product_id
    ).first()

    if cart_product:
        # Если товар уже в корзине, просто обновим количество и цену
        cart_product.quantity += quantity
        cart_product.price = price  # обновляем цену товара
    else:
        # Если товара нет в корзине, добавляем его
        db.execute(cart_product.insert().values(
            cart_id=cart_id, product_id=product_id, quantity=quantity, price=price
        ))

    db.commit()
    return {"message": "Product added to cart successfully."}

# Удаление товара из корзины
def remove_product_from_cart(db: Session, cart_id: int, product_id: int):
    db.execute(cart_product.delete().where(
        cart_product.c.cart_id == cart_id,
        cart_product.c.product_id == product_id
    ))
    db.commit()
    return {"message": "Product removed from cart successfully."}

# Получение всех товаров в корзине
def get_cart_items(db: Session, cart_id: int):
    products = db.query(Product).join(
        cart_product, cart_product.c.product_id == Product.id
    ).filter(cart_product.c.cart_id == cart_id).all()
    return products
