from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# We'll use SQLite for now, storing the DB file as health.db in the project root.
DB_FILENAME = "health.db"
DB_URL = f"sqlite:///{DB_FILENAME}"

# Create SQLAlchemy engine and session factory
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Yields a new SQLAlchemy Session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
