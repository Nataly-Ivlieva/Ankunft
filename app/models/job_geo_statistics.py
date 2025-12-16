from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class JobGeoStatistic(Base):
    __tablename__ = "job_geo_statistics"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    count = Column(Integer, nullable=False)
    category = relationship("Category")
    region = relationship("Region")
    city = relationship("City")