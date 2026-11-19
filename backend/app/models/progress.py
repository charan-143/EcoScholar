from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.session import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True)
    learner_id = Column(String(80), nullable=False, default="demo-learner", index=True)
    course_slug = Column(String(80), nullable=False, index=True)
    score = Column(Float, nullable=False)
    total = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
