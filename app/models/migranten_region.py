from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from .base import Base


class MigrantenRegion(Base):
    __tablename__ = "migranten_region"

    id = Column(Integer, primary_key=True)
    zusammen = Column(Float, nullable=True)
    arbeitslos = Column(Float, nullable=True)
    region_id = Column(Integer, ForeignKey("regions.id"))

    region = relationship("Region", back_populates="migranten_region", lazy="raise")