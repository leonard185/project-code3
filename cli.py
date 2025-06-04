# cli.py

import typer
from typing import Optional
from datetime import datetime
from sqlalchemy import func

from db import SessionLocal, engine
from models import Base, User, Entry, Goal, MealPlan, Reporting, ShowMeals

app = typer.Typer(help="Health Simplified CLI Application")


@app.command("init-db")
def init_db():
    """
    Create all tables in the database. Run this once before any other commands.
    """
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Database tables created.")

@app.command("show-mealplan")
def show_mealplan(
    user_id: int = typer.Option(..., "--user-id", "-u", help="ID of the user"),
    week:    int = typer.Option(..., "--week",    "-w", help="Week number of the plan"),
):
    """
    Display a table of planned meals for each day of the week (Monday–Sunday)
    for a given user_id and week.
    """
    db = SessionLocal()
    usr = db.query(User).filter(User.id == user_id).first()
    if not usr:
        typer.echo(f"❌ No user found with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    rows = (
        db.query(ShowMealPlan)
          .filter(ShowMealPlan.user_id == user_id, ShowMealPlan.week == week)
          .order_by(ShowMealPlan.week, ShowMealPlan.day_of_week)
          .all()
    )
    if not rows:
        typer.echo(f"⚠️  No meal plan found for user {user_id} in week {week}")
        db.close()
        return

    data = {
        "Day of Week": [r.day_of_week for r in rows],
        "Meals":       [r.meals for r in rows],
    }
    df = pd.DataFrame(data)
    db.close()
    typer.echo("Meal Plan:")


@app.command("create-user")
def create_user(name: str):
    """
    Create a new user with the given NAME.
    """
    db = SessionLocal()
    # Check for existing name to avoid duplicates (optional)
    existing = db.query(User).filter(User.name == name).first()
    if existing:
        typer.echo(f"❌ A user named '{name}' already exists (id={existing.id}).")
        db.close()
        raise typer.Exit(code=1)

    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    typer.echo(f"👍 Created user: {user.name}  (id={user.id})")
    db.close()


@app.command("list-users")
def list_users():
    """
    List all users in the database.
    """
    db = SessionLocal()
    users = db.query(User).all()
    if not users:
        typer.echo("No users found.")
    else:
        for u in users:
            typer.echo(f"{u.id}\t{u.name}")
    db.close()


@app.command("add-entry")
def add_entry(
    user_id: int,
    food: str,
    calories: int,
    date: str = typer.Argument(..., help="Date as YYYY-MM-DD"),
):
    """
    Add a food entry for a given USER_ID.
    """
    # Validate the date format
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit(code=1)

    db = SessionLocal()
    usr = db.query(User).filter(User.id == user_id).first()
    if not usr:
        typer.echo(f"❌ No user with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    entry = Entry(user_id=user_id, food=food, calories=calories, date=parsed_date)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    typer.echo(
        f"🍽️  Added entry: id={entry.id}, user_id={user_id}, "
        f"{food} ({calories} kcal) on {parsed_date}"
    )
    db.close()


@app.command("list-entries")
def list_entries(
    user_id: Optional[int] = typer.Option(None, help="Filter by user_id"),
    date: Optional[str] = typer.Option(None, help="Filter by date YYYY-MM-DD"),
):
    """
    List all food entries; optionally filter by --user-id or --date.
    """
    db = SessionLocal()
    query = db.query(Entry)

    if user_id is not None:
        query = query.filter(Entry.user_id == user_id)

    if date is not None:
        # Validate date string before querying
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            db.close()
            raise typer.Exit(code=1)
        query = query.filter(Entry.date == parsed_date)

    entries = query.all()
    if not entries:
        typer.echo("No entries found.")
    else:
        for e in entries:
            typer.echo(
                f"{e.id}\tuser_id={e.user_id}\t{e.food}\t"
                f"{e.calories} kcal\t{e.date}"
            )
    db.close()
    

@app.command("delete-entry")
def delete_entry(entry_id: int):
    """
    Delete a food entry by ENTRY_ID.
    """
    db = SessionLocal()
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        typer.echo(f"❌ No entry found with id={entry_id}")
        db.close()
        raise typer.Exit(code=1)
    db.delete(entry)
    db.commit()
    typer.echo(f"🗑️ Deleted entry with id={entry_id}")
    db.close()


@app.command("delete-user")
def delete_user(user_id: int):
    """
    Delete a user by USER_ID. (Also deletes related entries, goals, and meal plans!)
    """
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo(f"❌ No user found with id={user_id}")
        db.close()
        raise typer.Exit(code=1)
    db.delete(user)
    db.commit()
    typer.echo(f"🗑️ Deleted user with id={user_id} and related data.")
    db.close()

@app.command("create-goal")
def create_goal(
    user_id: int,
    daily: int,
    weekly: int
):
    """
    Add a daily and weekly goal for a given USER_ID.
    """
    from models import Goal  # Avoid circular import
    db = SessionLocal()

    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo(f"❌ No user with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    # Check if the user already has a goal
    existing_goal = db.query(Goal).filter(Goal.user_id == user_id).first()
    if existing_goal:
        typer.echo(f"❌ User already has a goal. Delete it first if you want to update.")
        db.close()
        raise typer.Exit(code=1)

    goal = Goal(user_id=user_id, daily=daily, weekly=weekly)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    typer.echo(
        f"🎯 Added goal: id={goal.id}, user_id={user_id}, daily={daily} kcal, weekly={weekly} kcal"
    )
    db.close()


@app.command("delete-goal")
def delete_goal(goal_id: int):
    """
    Delete a goal by GOAL_ID.
    """
    from models import Goal  # Import here to avoid circular import if needed
    db = SessionLocal()
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        typer.echo(f"❌ No goal found with id={goal_id}")
        db.close()
        raise typer.Exit(code=1)
    db.delete(goal)
    db.commit()
    typer.echo(f"🗑️ Deleted goal with id={goal_id}")
    db.close()


@app.command("delete-meal-plan")
def delete_meal_plan(meal_plan_id: int):
    """
    Delete a meal plan by MEAL_PLAN_ID.
    """
    from models import MealPlan  # Import here to avoid circular import if needed
    db = SessionLocal()
    meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not meal_plan:
        typer.echo(f"❌ No meal plan found with id={meal_plan_id}")
        db.close()
        raise typer.Exit(code=1)
    db.delete(meal_plan)
    db.commit()
    typer.echo(f"🗑️ Deleted meal plan with id={meal_plan_id}")
    db.close()

@app.command("add-meal-plan")
def add_meal_plan(
    user_id: int,
    week: int,
    plan_details: str = typer.Argument(..., help="Meal plan details"),
):
    """
    Add a meal plan for a given USER_ID and WEEK.
    """
    from models import MealPlan  # Import here to avoid circular import if needed
    db = SessionLocal()

    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo(f"❌ No user with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    meal_plan = MealPlan(user_id=user_id, week=week, plan_details=plan_details)
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    typer.echo(
        f"🍽️  Added meal plan: id={meal_plan.id}, user_id={user_id}, "
        f"week={week}, details='{plan_details or 'N/A'}'"
    )
    db.close()

# ────────────────────────────────────────────────────────────────────────────────
# Reporting commands
# ────────────────────────────────────────────────────────────────────────────────

@app.command("delete-report")
def delete_report(
    report_id: int = typer.Argument(..., help="ID of the report to delete"),
):
    """
    Delete a report entry by REPORT_ID.
    """
    db = SessionLocal()
    report = db.query(Reporting).filter(Reporting.id == report_id).first()
    if not report:
        typer.echo(f"❌ No report found with id={report_id}")
        db.close()
        raise typer.Exit(code=1)

    db.delete(report)
    db.commit()
    typer.echo(f"🗑️  Deleted report with id={report_id}")
    db.close()

@app.command("create-report")
def create_report(
    user_id: int = typer.Option(..., help="User ID for the report"),
    date: str = typer.Option(..., help="Date for the report in YYYY-MM-DD")
):
    """
    Create a daily report for a user by calculating total calories for the date.
    """
    from models import Reporting  # Avoid circular import
    from sqlalchemy import func  # Needed for sum

    db = SessionLocal()

    # Validate the date
    try:
        report_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        db.close()
        raise typer.Exit(code=1)

    # Check if the user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo(f"❌ No user found with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    # Check if report already exists
    existing_report = db.query(Reporting).filter(
        Reporting.user_id == user_id,
        Reporting.report_date == report_date
    ).first()

    if existing_report:
        typer.echo(
            f"⚠️ Report already exists for user_id={user_id} on {report_date} "
            f"(Total calories: {existing_report.total_calories})"
        )
        db.close()
        return

    # Calculate total calories for this date
    total_calories = db.query(func.sum(Entry.calories)).filter(
        Entry.user_id == user_id,
        Entry.date == report_date
    ).scalar()

    # If no entries found, total_calories will be None
    total_calories = total_calories or 0

    # Create the report entry
    report = Reporting(
        user_id=user_id,
        report_date=report_date,
        total_calories=total_calories
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    typer.echo("✅ Report created successfully:")
    typer.echo(f"  - User ID: {user_id}")
    typer.echo(f"  - Date: {report_date}")
    typer.echo(f"  - Total Calories: {total_calories}")
    db.close()


if __name__ == "__main__":
    app()


