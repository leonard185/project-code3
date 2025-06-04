from sqlalchemy.orm import Session
from models import Entry, Goal
from datetime import date

def report(session: Session, user_id: int):
    today = date.today()
    entries = session.query(Entry).filter_by(user_id=user_id, date=today).all()
    total_calories = sum(entry.calories for entry in entries)

    goal = session.query(Goal).filter_by(user_id=user_id).order_by(Goal.created_at.desc()).first()
    if not goal:
        print("No goals set.")
    else:
        print(f"Today's intake: {total_calories} calories.")
        print(f"Daily goal: {goal.daily} calories.")
        print(f"Weekly goal: {goal.weekly} calories.")
        print(f"Monthly goal: {goal.monthly} calories.")