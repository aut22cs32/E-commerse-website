
from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None
    price: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    image_url: Optional[str] = None
    stock: int = Field(default=0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    stock: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    image_url: Optional[str]
    stock: int
    is_active: bool

    class Config:
        from_attributes = True
