from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True) # Thêm ID làm Primary Key
    project_id = Column(Integer, ForeignKey("Projects.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String(50), nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Quan hệ
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")