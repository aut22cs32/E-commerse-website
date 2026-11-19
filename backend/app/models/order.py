from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_amount = Column(Numeric(10, 2), nullable=False)
    customer_name = Column(String(150), nullable=False, default="")
    address = Column(Text, nullable=False, default="")
    phone = Column(String(20), nullable=False, default="")
    payment_method = Column(String(50), nullable=False, default="Cash on Delivery")

    status = Column(
        String(50),
        default="Pending",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
