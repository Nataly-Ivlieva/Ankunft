from sqlalchemy import Column, Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class KursStat(Base):
    __tablename__ = "kurs_stat"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    count = Column(Float, nullable=False)

    protection_id = Column(Integer, ForeignKey("protection.id"))
    protection = relationship("Protection", back_populates="kurs_stat", lazy="raise")
