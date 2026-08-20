from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class ProjectMemberBase(BaseModel):
    role: str = "MEMBER"

class ProjectMemberCreate(ProjectMemberBase):
    project_id: int
    user_id: int

class ProjectMemberUpdate(BaseModel):
    role: str | None = None

class ProjectMemberResponse(ProjectMemberBase):
    project_id: int
    user_id: int
    joined_at: datetime
    user: UserResponse | None = None  # Trả về thông tin chi tiết thành viên

    class Config:
        from_attributes = True