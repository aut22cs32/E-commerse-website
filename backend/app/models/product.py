
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text

from app.database.connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
