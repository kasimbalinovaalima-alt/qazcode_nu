# src/ml_api_client.py - ПОЛНОСТЬЮ ОФЛАЙН ВЕРСИЯ
from typing import List, Dict, Any

class MLModelAPIClient:

    def __init__(self, api_url: str = None):
        # api_url больше не используется - мы в офлайне!
        print("✅ ОФЛАЙН-РЕЖИМ: нет внешних вызовов")
        print("📦 Модель будет загружена локально")
        self.offline_mode = True
        
        # Здесь ML команда будет загружать реальную модель
        self.model = None
        print("🔄 Заглушка: модель не загружена (ждем ML команду)")
    
    def predict(self, symptoms: str) -> List[Dict[str, Any]]:
        """
        Локальное предсказание БЕЗ ИНТЕРНЕТА
        """
        print(f"🔍 Локальный анализ симптомов: {symptoms}")
        
        # ВРЕМЕННАЯ ЗАГЛУШКА - потом ML команда заменит на реальную модель
        # Но это будет локальный вызов, без интернета!
        
        symptoms_lower = symptoms.lower()
        
        # Простая логика для демонстрации офлайн-работы
        if "кашель" in symptoms_lower and "температура" in symptoms_lower:
            return [
                {
                    "icd_code": "J06.9",
                    "name": "Острая инфекция верхних дыхательных путей",
                    "probability": 0.85,
                    "explanation": "Локальный анализ: кашель и температура типичны для ОРВИ"
                },
                {
                    "icd_code": "J15.9",
                    "name": "Пневмония",
                    "probability": 0.15,
                    "explanation": "Локальный анализ: если кашель влажный и температура держится"
                }
            ]
        elif "головная боль" in symptoms_lower:
            return [
                {
                    "icd_code": "G44.2",
                    "name": "Головная боль напряжения",
                    "probability": 0.70,
                    "explanation": "Локальный анализ: наиболее частая причина головной боли"
                },
                {
                    "icd_code": "G43.9",
                    "name": "Мигрень",
                    "probability": 0.30,
                    "explanation": "Локальный анализ: если боль пульсирующая и односторонняя"
                }
            ]
        else:
            return [
                {
                    "icd_code": "R69",
                    "name": "Неуточненное заболевание",
                    "probability": 1.0,
                    "explanation": "Локальный анализ: требуется дополнительное обследование"
                }
            ]

# Создаем глобальный экземпляр (теперь без URL - чисто офлайн!)
ml_api = MLModelAPIClient()