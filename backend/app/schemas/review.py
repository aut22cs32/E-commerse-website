from datetime import datetime
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    stars: int = Field(ge=1, le=5)
    review: str = Field(default="", max_length=300)


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    name: str
    stars: int
    review: str
    created_at: datetime
