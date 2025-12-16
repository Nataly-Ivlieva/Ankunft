from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    protection_id = Column(Integer, ForeignKey("protection.id"))


    protection = relationship("Protection", back_populates="country", lazy="raise")
    arbeit_stat = relationship("ArbeitStat", back_populates="country", lazy="raise")
