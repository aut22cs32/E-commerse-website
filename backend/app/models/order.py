from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func

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

    status = Column(
        String(50),
        default="Pending",
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


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