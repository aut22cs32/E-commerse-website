
from pydantic import BaseModel, Field
from app.schemas.product import ProductResponse


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True

# Update Cart Quantity Schema
class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)
