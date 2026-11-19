from datetime import datetime
from pydantic import BaseModel, Field


class ReturnRequestCreate(BaseModel):
    reason: str = Field(min_length=2, max_length=300)


class ReturnRequestResponse(BaseModel):
    id: int
    order_id: int
    order_item_id: int
    product_id: int
    product_name: str
    reason: str
    status: str
    created_at: datetime
