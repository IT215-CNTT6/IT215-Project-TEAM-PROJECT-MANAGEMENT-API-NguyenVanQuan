from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base schema chứa các thông tin cơ bản
class UserBase(BaseModel):
    email: str
    full_name: str  # Đã chuyển lên đây để dùng chung cho Create/Response

class UserCreate(UserBase):
    password: str
    role: str = "USER"
    is_active: bool = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None  # Đã sửa fullName -> full_name
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool 
    created_at: datetime
    class Config:
            from_attributes = True