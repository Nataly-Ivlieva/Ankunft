from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True)
    step = Column(Integer, nullable=False)
    question_text = Column(String(255), nullable=False)
    input_type = Column(String(50), nullable=False)
    select_api = Column(String(255), nullable=True)
    statistic_api = Column(String(255), nullable=True)
    answer_template = Column(String(500), nullable=True)
    positive_hint = Column(String(255), nullable=True)

