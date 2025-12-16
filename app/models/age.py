from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Age(Base):
    __tablename__ = "age"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    state_stat = relationship("StateStat", back_populates="age", lazy="raise")