
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

# Update Cart Quantity Schema
class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)