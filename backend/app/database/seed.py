from sqlalchemy import text

from app.database.connection import SessionLocal
from app.database.connection import engine
from app.models.product import Product


DEFAULT_PRODUCTS = [
    (1, "Laptop", "Electronics", 40000, "A reliable laptop for work, study and everyday use.", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=700&q=80", 10),
    (2, "Mobile", "Electronics", 20000, "A smartphone with a bright screen and a long-lasting battery.", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=700&q=80", 20),
    (3, "T-Shirt", "Fashion", 800, "A comfortable cotton t-shirt for everyday wear.", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=700&q=80", 30),
    (4, "Cricket Bat", "Sports", 2500, "A balanced cricket bat for practice and matches.", "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=700&q=80", 8),
    (5, "Cookware Set", "Home & Kitchen", 3499, "A practical cookware set for everyday home cooking.", "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=700&q=80", 12),
    (6, "Table Lamp", "Home & Kitchen", 1299, "A warm table lamp for your bedside or reading corner.", "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=700&q=80", 15),
    (7, "Bestseller Novel", "Books", 499, "A page-turning novel to add to your reading list.", "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&w=700&q=80", 25),
    (8, "Daily Journal", "Books", 299, "A hardcover journal for notes, plans and ideas.", "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=700&q=80", 25),
    (9, "Skincare Set", "Beauty", 999, "A simple skincare set for your daily routine.", "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?auto=format&fit=crop&w=700&q=80", 18),
    (10, "Perfume", "Beauty", 1499, "A fresh everyday fragrance in a travel-friendly bottle.", "https://images.unsplash.com/photo-1541643600914-78b084683601?auto=format&fit=crop&w=700&q=80", 15),
    (11, "Coffee Beans", "Groceries", 599, "Roasted coffee beans for a rich cup at home.", "https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=700&q=80", 40),
    (12, "Organic Honey", "Groceries", 349, "Naturally sweet honey for drinks and breakfast.", "https://images.unsplash.com/photo-1587049352851-8d4e89133924?auto=format&fit=crop&w=700&q=80", 40),
    (13, "Building Blocks", "Toys", 899, "Colorful building blocks for creative play.", "https://images.unsplash.com/photo-1587654780291-39c9404d746b?auto=format&fit=crop&w=700&q=80", 20),
    (14, "Teddy Bear", "Toys", 699, "A soft plush teddy bear made for cuddles.", "https://images.unsplash.com/photo-1559454403-b8fb88521f11?auto=format&fit=crop&w=700&q=80", 20),
    (15, "Wrist Watch", "Accessories", 2199, "A clean everyday wrist watch with a classic design.", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=700&q=80", 12),
    (16, "Sunglasses", "Accessories", 999, "Lightweight sunglasses for sunny days out.", "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=700&q=80", 12),
]


def seed_products():
    db = SessionLocal()
    try:
        for product_id, name, category, price, description, image_url, stock in DEFAULT_PRODUCTS:
            exists = db.query(Product).filter(Product.id == product_id).first()
            if exists is None:
                db.add(Product(
                    id=product_id,
                    name=name,
                    category=category,
                    price=price,
                    description=description,
                    image_url=image_url,
                    stock=stock,
                    is_active=True,
                ))
        db.commit()
        if engine.dialect.name == "postgresql":
            db.execute(text(
                "SELECT setval(pg_get_serial_sequence('products', 'id'), "
                "GREATEST((SELECT COALESCE(MAX(id), 1) FROM products), 1), true)"
            ))
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
