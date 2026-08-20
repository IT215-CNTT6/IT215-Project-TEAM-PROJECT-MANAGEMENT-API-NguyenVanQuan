from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: str
    status: str = "todo"
    priority: str = "medium"
    due_date: datetime | None = None

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None

class TaskResponse(TaskBase):
    id: int
    project_id: int
    assignee_id: int | None = None
    created_at: datetime
    assignee: UserResponse | None = None 

    class Config:
        from_attributes = True