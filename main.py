from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

app = FastAPI(title="Налоговый Аналитик 2.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/incomes/", response_model=schemas.IncomeOut) # <-- Проверь этот путь
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return crud.create_income(db=db, income=income)

@app.get("/forecast/", response_model=schemas.TaxForecast)
def get_tax_forecast(db: Session = Depends(get_db)):
    db_incomes = crud.get_user_incomes(db)
    
    if len(db_incomes) < 2:
        raise HTTPException(status_code=400, detail="Недостаточно данных для мат. моделирования")

    # --- 1. Сбор и сортировка данных ---
    sorted_data = sorted(db_incomes, key=lambda x: x.received_at)
    amounts = [i.amount for i in sorted_data]
    fact_total = sum(amounts)
    
    # Гипотеза расходов (для оптимизации): допустим, расходы составляют 40% от дохода
    # В реальной системе это поле бралось бы из БД
    estimated_expenses = fact_total * 0.4 

    # --- 2. Учет СЛУЧАЙНЫХ ЯВЛЕНИЙ (EMA - Экспоненциальное сглаживание) ---
    alpha = 0.3
    ema = amounts[0]
    for i in range(1, len(amounts)):
        ema = alpha * amounts[i] + (1 - alpha) * ema
    
    # Прогноз на квартал (3 мес) на основе сглаженного тренда
    predicted_future_income = ema * 3

    # --- 3. ДЕТЕРМИНИРОВАННЫЙ РАСЧЕТ И ОПТИМИЗАЦИЯ РЕЖИМОВ ---
    # Общий ожидаемый доход (Факт + Прогноз)
    total_expected_revenue = fact_total + predicted_future_income
    
    # Сценарий А: УСН 6%
    tax_usn_6 = total_expected_revenue * 0.06
    
    # Сценарий Б: УСН 15% (Доходы - Расходы)
    # Считаем налог с прибыли, учитывая минимальный налог 1%
    profit = total_expected_revenue - (estimated_expenses + (estimated_expenses/len(amounts)*3))
    tax_usn_15 = max(profit * 0.15, total_expected_revenue * 0.01)

    # --- 4. ВЫБОР ЛУЧШЕГО ПРОЕКТНОГО РЕШЕНИЯ ---
    best_tax = min(tax_usn_6, tax_usn_15)
    savings = abs(tax_usn_6 - tax_usn_15)
    best_regime = "УСН 6%" if tax_usn_6 < tax_usn_15 else "УСН 15%"

    return {
        "total_income_fact": round(fact_total, 2),
        "predicted_income_future": round(predicted_future_income, 2),
        "estimated_tax": round(best_tax, 2),
        "recommended_regime": best_regime,
        "potential_savings": round(savings, 2),
        "recommendation": f"Алгоритм EMA выявил тренд. Рекомендуется режим {best_regime}. Экономия: {round(savings, 2)} руб."
    }