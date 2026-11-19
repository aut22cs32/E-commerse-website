from pydantic import BaseModel, EmailStr, Field


# Register Schema
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


# Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
