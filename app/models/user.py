from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("SessionToken", back_populates="user", cascade="all, delete-orphan")
