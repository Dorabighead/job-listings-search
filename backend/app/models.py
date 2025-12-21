from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String(100), unique=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    location = Column(String(100), index=True)
    experience = Column(String(50))
    education = Column(String(50))
    job_type = Column(String(50))
    description = Column(Text)
    requirements = Column(Text)
    welfare = Column(Text)
    source = Column(String(50), index=True)
    url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    favorites = relationship("Favorite", back_populates="job", cascade="all, delete-orphan")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="favorites")
