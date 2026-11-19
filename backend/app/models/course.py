from sqlalchemy import Column, Integer, String, Text
from app.db.session import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(80), unique=True, nullable=False, index=True)
    title = Column(String(180), nullable=False)
    category = Column(String(80), nullable=False)
    level = Column(String(40), nullable=False)
    duration = Column(String(40), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
