# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (SQLite)
DATABASE_URL = "sqlite:///health.db"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
