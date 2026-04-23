from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func 
from app.core.database import Base

class TriageSession(Base):
	__tablename__ = "triage_sessions"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	symptom = Column(String, nullable=False)
	duration = Column(String, nullable=False)
	severity = Column(Integer, nullable=False)
	details = Column(Text, nullable=True)
	age = Column(Integer, nullable=False)
	known_conditions = Column(Text, nullable=True)
	urgency_level = Column(String, nullable=False)
	recommendation = Column(Text, nullable=False)
	reasoning = Column(Text, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())

	user = relationship("User", back_populates="sessions")