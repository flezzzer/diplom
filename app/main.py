from fastapi import FastAPI
from app.api.v1 import user, product, order, reviews, cart, auth, category, sellers
from app.db.session import init_db

app = FastAPI()

# Подключение роутов
app.include_router(user.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(category.router)
app.include_router(reviews.router)
app.include_router(cart.router)
app.include_router(auth.router)
app.include_router(sellers.router)

# Инициализация базы данных
init_db()
