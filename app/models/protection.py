from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Protection(Base):
    __tablename__ = "protection"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    country = relationship("Country", back_populates="protection", lazy="raise")
    kurs_stat = relationship("KursStat", back_populates="protection", lazy="raise")
    state_stat = relationship("StateStat", back_populates="protection", lazy="raise")