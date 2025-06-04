from sqlalchemy.orm import Session
from models import Goal
from datetime import datetime

def set_goal(session: Session, user_id: int, daily: int, weekly: int):
    goal = Goal(user_id=user_id, daily=daily, weekly=weekly, created_at=datetime.utcnow())
    session.add(goal)
    session.commit()
    print("Goals set successfully.")
