from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from app.database.connection import Base


class ReturnRequest(Base):
    __tablename__ = "return_requests"
    __table_args__ = (UniqueConstraint("order_item_id", name="uq_return_order_item"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    reason = Column(String(300), nullable=False)
    status = Column(String(50), nullable=False, default="Return requested")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
