from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
class Base(DeclarativeBase):
	pass

# Dependency to get DB session
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()