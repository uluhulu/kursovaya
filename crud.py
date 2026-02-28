from sqlalchemy.orm import Session
import models, schemas

# Функция создания записи (Прямое проектирование объекта)
def create_income(db: Session, income: schemas.IncomeCreate):
    # Преобразуем Pydantic-объект в модель SQLAlchemy
    db_income = models.Income(
        amount=income.amount,
        category=income.category,
        received_at=income.received_at,
        is_atypical=income.is_atypical
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

# Функция получения данных для "Умного прогноза"
def get_user_incomes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Income).offset(skip).limit(limit).all()