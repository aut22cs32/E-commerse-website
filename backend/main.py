
from fastapi import FastAPI

from app.database.connection import engine, Base
from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.routes.auth import router as auth_router
from app.routes.products import router as product_router
from app.routes.cart import router as cart_router
from app.models.order import Order, OrderItem
from app.routes.orders import router as order_router

app = FastAPI(
    title="E-Commerce Backend API",
    description="Backend API for E-Commerce Application",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to E-Commerce Backend API",
        "database": "PostgreSQL Connected"
    }
