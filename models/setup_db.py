# setup_db.py
from db import engine
from models import Base

def create_tables():
    Base.metadata.create_all(engine)
    print("✅ Database tables created!")

if __name__ == "__main__":
    create_tables()
