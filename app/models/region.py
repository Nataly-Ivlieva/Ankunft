from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    cities = relationship("City", back_populates="region", lazy="raise")
    salary_statistics = relationship("SalaryStatistic", back_populates="region", lazy="raise")
    migranten_region = relationship("MigrantenRegion", back_populates="region", lazy="raise")
