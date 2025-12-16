from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
from .base import Base
import enum

class ArbeitState(enum.Enum):
    beschaeftigte = "Beschäftigte"
    teilzeit = "Teilzeit"
    unterbeschaeftigte = "Unterbeschäftigte"

class ArbeitStat(Base):
    __tablename__ = "arbeit_stat"

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    country = relationship("Country", back_populates="arbeit_stat")
    count = Column(Float, nullable=False)
    name = Column(Enum(ArbeitState), nullable=False)