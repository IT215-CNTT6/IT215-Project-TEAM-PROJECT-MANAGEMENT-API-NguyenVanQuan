from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"

    # Khoá chính hợp phần (Composite PK)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(VARCHAR(50), nullable=False)  # OWNER / MEMBER
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Mối quan hệ
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="memberships")