from sqlalchemy import Boolean, Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    is_verified = Column(Boolean, default=False)
    login_attempts = Column(Integer, default=0)
    is_blocked = Column(Boolean, default=False)
    blocked_until = Column(DateTime, default=None)
    email_attempts = Column(Integer, default=0)
    last_email_attempt = Column(DateTime, default=None)
    otp = Column(String, default=None)
    otp_expiry = Column(DateTime, default=None)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    role = Column(String, default="user")

    projects = relationship("Project", back_populates="creator")
    assigned_tasks = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")  # Tasks assigned to them
