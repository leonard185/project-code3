# seed.py
from db import SessionLocal
from models import User, Entry
from datetime import date

def seed():
    db = SessionLocal()
    user = User(name="Alice")
    db.add(user)
    db.commit()
    db.refresh(user)

    entry = Entry(user_id=user.id, food="Salad", calories=300, date=date.today())
    db.add(entry)
    db.commit()
    db.close()
    print("✅ Seed data created.")

if __name__ == "__main__":
    seed()
