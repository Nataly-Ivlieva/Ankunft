from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SalaryStatistic(Base):
    __tablename__ = "salary_statistics"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    month = Column(String)
    salary = Column(Float)

    region = relationship("Region", back_populates="salary_statistics")
    category = relationship("Category", back_populates="salary_statistics")


