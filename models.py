from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
# ВАЖНО: Импортируем Base из нашего файла database.py
from database import Base 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    # ... остальные поля

class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String)
    received_at = Column(Date)
    is_atypical = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))