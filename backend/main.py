from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from app.database.connection import Base, engine
from app.database.seed import seed_products
from app.models import CartItem, Order, OrderItem, Product, ReturnRequest, Review, User, WishlistItem
from app.routes.auth import router as auth_router
from app.routes.cart import router as cart_router
from app.routes.orders import router as order_router
from app.routes.products import router as product_router
from app.routes.reviews import router as review_router
from app.routes.returns import router as return_router
from app.routes.wishlist import router as wishlist_router


def prepare_database():
    Base.metadata.create_all(bind=engine)

    # Add fields for existing databases created by the earlier backend version.
    columns = {column["name"] for column in inspect(engine).get_columns("orders")}
    user_columns = {column["name"] for column in inspect(engine).get_columns("users")}
    with engine.begin() as connection:
        if "is_admin" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT FALSE"))
        if "customer_name" not in columns:
            connection.execute(text("ALTER TABLE orders ADD COLUMN customer_name VARCHAR(150) NOT NULL DEFAULT ''"))
        if "address" not in columns:
            connection.execute(text("ALTER TABLE orders ADD COLUMN address TEXT NOT NULL DEFAULT ''"))
        if "phone" not in columns:
            connection.execute(text("ALTER TABLE orders ADD COLUMN phone VARCHAR(20) NOT NULL DEFAULT ''"))
        if "payment_method" not in columns:
            connection.execute(
                text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'Cash on Delivery'")
            )
        admin_email = os.getenv("ADMIN_EMAIL", "").strip().lower()
        if admin_email:
            connection.execute(
                text("UPDATE users SET is_admin = TRUE WHERE lower(email) = :email"),
                {"email": admin_email},
            )

    seed_products()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    prepare_database()
    yield


app = FastAPI(
    title="Our Store API",
    description="Backend API for the ecommerce website",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(return_router)
app.include_router(wishlist_router)


@app.get("/")
def home():
    return {"message": "Our Store API is running"}
