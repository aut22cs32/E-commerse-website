from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime
from app.schemas.product import ProductResponse


# Order Item Schema
class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: ProductResponse

    class Config:
        from_attributes = True


# Order Response Schema
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    customer_name: str
    address: str
    phone: str
    payment_method: str
    items: List[OrderItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

# Order Details Schema
class OrderDetailResponse(OrderResponse):
    items: List[OrderItemResponse] = []


class PlaceOrderRequest(BaseModel):
    customer_name: str = Field(min_length=1, max_length=150)
    address: str = Field(min_length=5, max_length=1000)
    phone: str = Field(pattern=r"^\d{10}$")
    payment_method: Literal["Cash on Delivery"] = "Cash on Delivery"
