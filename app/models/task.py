from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks" # Đã sửa tên bảng trùng lặp từ "users" thành "tasks"

    id = Column(Integer, primary_key=True, index=True) # Đã sửa id làm khóa chính chính
    project_id = Column(Integer, ForeignKey("Projects.id"), nullable=True)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Đã sửa thành ForeignKey trỏ về users.id
    status = Column(VARCHAR(50), nullable=False)
    priority = Column(VARCHAR(50), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Quan hệ
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")