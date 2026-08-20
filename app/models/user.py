from sqlalchemy import Column, Integer, VARCHAR, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    password_hash = Column(VARCHAR(255), nullable=False)
    full_name = Column(VARCHAR(100), nullable=False)
    role = Column(VARCHAR(50), default="USER", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Mối quan hệ
    projects_owned = relationship("Project", back_populates="owner")
    tasks_assigned = relationship("Task", back_populates="assignee")
    memberships = relationship("ProjectMember", back_populates="user")
