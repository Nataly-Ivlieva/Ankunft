from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    label = Column(String(255), unique=True, nullable=False)
    tag = Column(String(255), unique=True, nullable=False)

    salary_statistics = relationship("SalaryStatistic", back_populates="category")