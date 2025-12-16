from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    state_stat = relationship("StateStat", back_populates="genders", lazy="raise")