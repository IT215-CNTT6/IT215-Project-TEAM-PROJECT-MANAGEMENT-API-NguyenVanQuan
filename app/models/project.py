from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    description = Column(Text, nullable=True)  # Mặc định NULL theo thiết kế
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # FK đến users.id
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Mối quan hệ
    owner = relationship("User", back_populates="projects_owned")
    tasks = relationship("Task", back_populates="project")
    members = relationship("ProjectMember", back_populates="project")