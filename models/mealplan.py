# mealplan.py
from sqlalchemy.orm import Session
from models import User, MealPlan

def create_meal_plan(db: Session, user_name: str, week: int, plan_details: str):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        return None, f"User '{user_name}' not found."

    meal_plan = MealPlan(user_id=user.id, week=week, plan_details=plan_details)
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan, None

def list_meal_plans(db: Session, user_name: str):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        return None, f"User '{user_name}' not found."

    meal_plans = db.query(MealPlan).filter(MealPlan.user_id == user.id).all()
    return meal_plans, None
