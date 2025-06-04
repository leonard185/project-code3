# main.py
import typer
from sqlalchemy.orm import Session
from db import SessionLocal
from models import User, Entry
from datetime import date

app = typer.Typer()

@app.command()
def create_user(name: str):
    """
    Create a new user.
    """
    db: Session = SessionLocal()
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    typer.echo(f"User '{name}' created with ID {user.id}")

@app.command()
def list_users():
    """
    List all users.
    """
    db: Session = SessionLocal()
    users = db.query(User).all()
    db.close()
    if users:
        for user in users:
            typer.echo(f"{user.id}: {user.name}")
    else:
        typer.echo("No users found.")

@app.command()
def add_entry(user_name: str, food: str, calories: int, entry_date: str):
    """
    Add a food entry.
    """
    db: Session = SessionLocal()
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        typer.echo(f"User '{user_name}' not found!")
        db.close()
        return
    entry = Entry(user_id=user.id, food=food, calories=calories, date=date.fromisoformat(entry_date))
    db.add(entry)
    db.commit()
    db.refresh(entry)
    db.close()
    typer.echo(f"Entry '{food}' with {calories} calories added for {entry_date}")

@app.command()
def list_entries(user_name: str = None):
    """
    List food entries.
    """
    db: Session = SessionLocal()
    if user_name:
        user = db.query(User).filter(User.name == user_name).first()
        if not user:
            typer.echo(f"User '{user_name}' not found!")
            db.close()
            return
        entries = db.query(Entry).filter(Entry.user_id == user.id).all()
    else:
        entries = db.query(Entry).all()
    db.close()
    if entries:
        for e in entries:
            typer.echo(f"{e.id}: {e.food}, {e.calories} cal, {e.date}")
    else:
        typer.echo("No entries found.")

if __name__ == "__main__":
    app()
