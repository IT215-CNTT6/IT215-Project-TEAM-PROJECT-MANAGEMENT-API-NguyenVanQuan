from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    fullName: str

class UserCreate(UserBase):
    password: str
    role: str = "user"

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    fullName: str | None = None
    password: str | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True