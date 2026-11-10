from pydantic import BaseModel
from typing import List
from datetime import datetime


# Order Item Schema
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


# Order Response Schema
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Order Details Schema
class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse] = []