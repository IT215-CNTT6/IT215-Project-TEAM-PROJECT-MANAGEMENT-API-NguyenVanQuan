from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class ProjectBase(BaseModel):
    name: str
    description: str

class ProjectCreate(ProjectBase):
    user_id: int | None = None

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectResponse(ProjectBase):
    id: int
    user_id: int | None = None
    created_at: datetime
    owner: UserResponse | None = None  # Trả về thông tin Owner (nested)

    class Config:
        from_attributes = True