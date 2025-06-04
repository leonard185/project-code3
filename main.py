# main.py

import typer
from typing import Optional

from db import SessionLocal, engine
from models import Base, User, Entry

app = typer.Typer(help="Health Simplified CLI Application")

@app.command("init-db")
def init_db():
    """
    Create all tables in the database. Run this once before any other commands.
    """
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Database tables created.")

@app.command("create-user")
def create_user(name: str):
    """
    Create a new user with the given NAME.
    """
    db = SessionLocal()
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
    db = SessionLocal()
    usr = db.query(User).filter(User.id == user_id).first()
    if not usr:
        typer.echo(f"❌ No user with id={user_id}")
        db.close()
        raise typer.Exit(code=1)

    entry = Entry(user_id=user_id, food=food, calories=calories, date=date)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    typer.echo(f"🍽️  Added entry: id={entry.id}, user_id={user_id}, {food} ({calories} kcal) on {date}")
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
        query = query.filter(Entry.date == date)
    entries = query.all()

    if not entries:
        typer.echo("No entries found.")
    else:
        for e in entries:
            typer.echo(f"{e.id}\tuser_id={e.user_id}\t{e.food}\t{e.calories} kcal\t{e.date}")
    db.close()

if __name__ == "__main__":
    app()
