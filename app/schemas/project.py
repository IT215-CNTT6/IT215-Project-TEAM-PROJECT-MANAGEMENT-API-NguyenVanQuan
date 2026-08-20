from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class ProjectBase(BaseModel):
    name: str
    description: str | None = None  # Đã sửa cho phép NULL theo CSDL

class ProjectCreate(ProjectBase):
    pass  # Thông thường owner_id sẽ tự động lấy từ Token đăng nhập (current_user)

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int                   # Đã sửa user_id thành owner_id (NOT NULL)
    created_at: datetime
    owner: UserResponse | None = None  # Trả về thông tin Owner (nested)

    
    class Config:
            from_attributes = True