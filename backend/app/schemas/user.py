from pydantic import BaseModel, EmailStr


# Register Schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response Schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True