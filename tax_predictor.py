import math

class TaxPredictor:
    def __init__(self, tax_rate: float, historical_data: list):
        self.tax_rate = tax_rate
        self.data = historical_data # Список сумм за прошлые месяцы

    def get_seasonal_index(self, month: int) -> float:
        """Метод системного анализа: вычисление индекса сезонности"""
        if not self.data: return 1.0
        avg_income = sum(self.data) / len(self.data)
        # В реальности здесь была бы логика сравнения месяца с прошлыми годами
        return self.data[month % len(self.data)] / avg_income if avg_income > 0 else 1.0

    def predict_tax(self, months_remaining: int) -> float:
        """Математическая модель детерминированного и случайного процесса"""
        # Экспоненциальное сглаживание для базового уровня
        alpha = 0.3
        base_level = self.data[-1] if self.data else 0
        
        predicted_income = 0
        for i in range(1, months_remaining + 1):
            # Умножаем базу на сезонный коэффициент
            seasonal_factor = self.get_seasonal_index(len(self.data) + i)
            predicted_income += base_level * seasonal_factor
            
        return predicted_income * self.tax_rate

# Пример использования
predictor = TaxPredictor(tax_rate=0.06, historical_data=[1000, 1200, 800, 1500])
print(f"Ожидаемый налог за остаток года: {predictor.predict_tax(3)}")