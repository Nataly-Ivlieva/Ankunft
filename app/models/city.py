from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="cities", lazy="raise")
