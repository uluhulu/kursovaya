from pydantic import BaseModel, Field, validator
from datetime import date
from typing import List, Optional

# --- Схемы для Доходов ---

class IncomeBase(BaseModel):
    """Базовые поля, общие для всех операций"""
    amount: float = Field(..., gt=0, description="Сумма должна быть положительной")
    category: str = Field(..., min_length=2)
    received_at: date
    is_atypical: bool = False

class IncomeCreate(IncomeBase):
    """То, что присылает фронтенд при создании записи"""
    pass

class IncomeOut(IncomeBase):
    """То, что API отдает назад (добавляем ID из базы)"""
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True # Позволяет преобразовывать объекты SQLAlchemy в Pydantic

# --- Схемы для Пользователей ---

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    """Регистрация: передаем еще и пароль"""
    password: str
    tax_regime: str = "self_employed"

class UserOut(UserBase):
    id: int
    tax_regime: str

    class Config:
        from_attributes = True

# --- Схема Прогноза (Результат алгоритма) ---

# schemas.py
class TaxForecast(BaseModel):
    total_income_fact: float
    predicted_income_future: float
    estimated_tax: float
    recommended_regime: str  # Новое!
    potential_savings: float  # Новое!
    recommendation: str