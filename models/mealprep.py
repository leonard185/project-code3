from sqlalchemy.orm import Session
from models import MealPlan

def add_meal_plan(session: Session, user_id: int, week: str, plan_details: str):
    plan = MealPlan(user_id=user_id, week=week, plan_details=plan_details)
    session.add(plan)
    session.commit()
    print(f"Meal plan for {week} added.")

def view_meal_plans(session: Session, user_id: int):
    plans = session.query(MealPlan).filter_by(user_id=user_id).all()
    for plan in plans:
        print(f"Week: {plan.week}")
        print(f"Plan: {plan.plan_details}")
        print("-" * 20)
def delete_meal_plan(session: Session, user_id: int, week: str):
    plan = session.query(MealPlan).filter_by(user_id=user_id, week=week).first()
    if plan:
        session.delete(plan)
        session.commit()
        print(f"Meal plan for {week} deleted.")
    else:
        print(f"No meal plan found for week: {week}.")  