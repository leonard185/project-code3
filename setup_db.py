from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Database setup
DB_FILENAME = "health.db"
DB_URL = f"sqlite:///{DB_FILENAME}"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    entries = relationship("Entry", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    show_meal_plans = relationship(
        "ShowMealPlan",
        back_populates="user",
        cascade="all, delete-orphan",
    )

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    user = relationship("User", back_populates="entries")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily = Column(Integer, nullable=False)
    weekly = Column(Integer, nullable=False)
    user = relationship("User", back_populates="goals")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week = Column(Integer, nullable=False)
    plan_details = Column(String, nullable=True)
    user = relationship("User", back_populates="meal_plans")

class Reporting(Base):
    __tablename__ = "reporting"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    total_calories = Column(Integer, nullable=False)
    user = relationship("User")

class ShowMealPlan(Base):
    __tablename__ = "show_meal_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_of_week = Column(String, nullable=False)  # e.g. "Monday", "Tuesday", etc.
    meals= Column(String, nullable=False) 
    user = relationship("User")

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"Database {DB_FILENAME} and tables created!")

if __name__ == "__main__":
    init_db()
