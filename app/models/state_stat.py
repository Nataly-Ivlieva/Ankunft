from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from .base import Base
import enum

class ArbeitState(enum.Enum):
    arbeitslose = "Arbeitslose"
    migranten = "Migranten"

class  StateStat(Base):
    __tablename__ = "state_stat"

    id = Column(Integer, primary_key=True)
    age_id = Column(Integer, ForeignKey("age.id"), nullable=True)
    age = relationship("Age", back_populates="state_stat")
    gender_id = Column(Integer, ForeignKey("genders.id"), nullable=True)
    genders = relationship("Gender", back_populates="state_stat")
    protection_id = Column(Integer, ForeignKey("protection.id"), nullable=False)
    protection = relationship("Protection", back_populates="state_stat")
    count = Column(Float, nullable=False)
    name = Column(Enum(ArbeitState,values_callable=lambda enum: [e.value for e in enum]),nullable=False)