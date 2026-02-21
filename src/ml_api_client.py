# src/ml_api_client.py
import httpx
from typing import List, Dict, Any
import asyncio

class MLModelAPIClient:
    """
    Клиент для подключения к API ML модели
    """
    
    def __init__(self, api_url: str = "http://ml-service:8000/predict"):
        """
        Инициализация клиента
        
        Args:
            api_url: URL где будет доступна ML модель
                    Например: "http://localhost:8002/predict"
                    Или: "http://ml-container:8000/predict"
        """
        self.api_url = api_url
        self.client = httpx.Client(timeout=30.0)
        print(f"🔄 ML API клиент инициализирован. URL: {api_url}")
    
    def predict(self, symptoms: str) -> List[Dict[str, Any]]:
        """
        Отправляет симптомы в ML API и получает диагнозы
        
        Args:
            symptoms: строка с симптомами
            
        Returns:
            Список диагнозов в формате:
            [
                {
                    "icd_code": "J06.9",
                    "name": "Диагноз",
                    "probability": 0.85,
                    "explanation": "Объяснение"
                }
            ]
        """
        try:
            # Отправляем POST запрос к ML API
            response = self.client.post(
                self.api_url,
                json={"symptoms": symptoms}
            )
            
            # Проверяем ответ
            response.raise_for_status()
            
            # Получаем результат
            result = response.json()
            
            # Ожидаем, что ML API вернет список диагнозов
            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "diagnoses" in result:
                return result["diagnoses"]
            else:
                print(f"❌ Неожиданный формат ответа: {result}")
                return self._fallback_response(symptoms)
                
        except Exception as e:
            print(f"❌ Ошибка при обращении к ML API: {e}")
            return self._fallback_response(symptoms)
    
    def _fallback_response(self, symptoms: str) -> List[Dict[str, Any]]:
        """
        Запасной вариант, если API недоступен
        """
        return [
            {
                "icd_code": "R69",
                "name": "Неуточненное заболевание",
                "probability": 1.0,
                "explanation": f"ML API недоступно. Симптомы: {symptoms}"
            }
        ]
    
    def __del__(self):
        """Закрываем соединение при удалении объекта"""
        if hasattr(self, 'client'):
            self.client.close()


# !!! ВАЖНО: ЗАМЕНИТЕ URL НА РЕАЛЬНЫЙ АДРЕС ML API !!!
ml_api = MLModelAPIClient(api_url="http://localhost:8002/predict")