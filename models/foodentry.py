# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    entries = relationship('Entry', back_populates='user', cascade='all, delete-orphan')
    goals = relationship('Goal', back_populates='user', cascade='all, delete-orphan')
    meal_plans = relationship('MealPlan', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Entry(Base):
    __tablename__ = 'entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    user = relationship('User', back_populates='entries')

    def __repr__(self):
        return f"<Entry(id={self.id}, food='{self.food}', calories={self.calories}, date={self.date})>"

class Goal(Base):
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    daily = Column(Integer, nullable=False)
    weekly = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship('User', back_populates='goals')

    def __repr__(self):
        return f"<Goal(id={self.id}, daily={self.daily}, weekly={self.weekly})>"

class MealPlan(Base):
    __tablename__ = 'meal_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week = Column(Integer, nullable=False)
    plan_details = Column(Text, nullable=True)
    
    user = relationship('User', back_populates='meal_plans')

    def __repr__(self):
        return f"<MealPlan(id={self.id}, week={self.week})>"
