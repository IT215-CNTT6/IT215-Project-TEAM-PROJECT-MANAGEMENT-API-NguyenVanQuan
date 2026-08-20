from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=True)  # Mặc định NULL theo thiết kế
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Cho phép NULL
    status = Column(VARCHAR(50), nullable=False)  # TODO / IN_PROGRESS / DONE
    priority = Column(VARCHAR(50), nullable=False)  # LOW / MEDIUM / HIGH
    due_date = Column(DateTime, nullable=True)  # Cho phép NULL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Mối quan hệ
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")