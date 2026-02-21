from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

# Импортируем клиент для ML API
try:
    from ml_api_client import ml_api
    ML_API_AVAILABLE = True
    print(f"✅ ML API клиент загружен. URL: {ml_api.api_url}")
except ImportError as e:
    ML_API_AVAILABLE = False
    print(f"⚠️ ML API клиент не загружен: {e}")
    
    # Заглушка на случай отсутствия API
    def get_fallback_diagnoses(symptoms: str):
        return [
            {
                "icd_code": "R69",
                "name": "Неуточненное заболевание",
                "probability": 1.0,
                "explanation": f"ML API не доступно. Используется заглушка. Симптомы: {symptoms}"
            }
        ]

# Создаем приложение
app = FastAPI(title="Medical Diagnosis Assistant")

# Разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class SymptomRequest(BaseModel):
    symptoms: str

class Diagnosis(BaseModel):
    icd_code: str
    name: str
    probability: float
    explanation: str

class DiagnosisResponse(BaseModel):
    diagnoses: List[Diagnosis]

# Новые модели для запроса объяснения
class ExplanationRequest(BaseModel):
    symptoms: str
    icd_code: str
    diagnosis_name: str

class ExplanationResponse(BaseModel):
    explanation: str

# ВРЕМЕННАЯ ЗАГЛУШКА - ЗДЕСЬ БУДЕТ ML МОДЕЛЬ
def get_mock_diagnoses(symptoms: str) -> List[Dict[str, Any]]:
    """
    Временная функция, которая будет заменена на ML модель
    """
    symptoms = symptoms.lower()
    
    # База знаний на основе симптомов
    if "кашель" in symptoms and "температура" in symptoms:
        return [
            {
                "icd_code": "J06.9",
                "name": "Острая инфекция верхних дыхательных путей",
                "probability": 0.85,
                "explanation": "Кашель и температура типичны для ОРВИ"
            },
            {
                "icd_code": "J15.9",
                "name": "Пневмония",
                "probability": 0.15,
                "explanation": "Если кашель влажный и температура высокая"
            }
        ]
    elif "головная боль" in symptoms:
        return [
            {
                "icd_code": "G44.2",
                "name": "Головная боль напряжения",
                "probability": 0.70,
                "explanation": "Наиболее частая причина головной боли"
            },
            {
                "icd_code": "G43.9",
                "name": "Мигрень",
                "probability": 0.30,
                "explanation": "Если боль пульсирующая и односторонняя"
            }
        ]
    elif "боль в горле" in symptoms:
        return [
            {
                "icd_code": "J02.9",
                "name": "Острый фарингит",
                "probability": 0.80,
                "explanation": "Воспаление глотки"
            },
            {
                "icd_code": "J03.9",
                "name": "Острый тонзиллит",
                "probability": 0.20,
                "explanation": "Если есть налет на миндалинах"
            }
        ]
    elif "насморк" in symptoms or "заложенность носа" in symptoms:
        return [
            {
                "icd_code": "J00",
                "name": "Острый назофарингит (насморк)",
                "probability": 0.90,
                "explanation": "Воспаление слизистой носа и глотки"
            },
            {
                "icd_code": "J30.1",
                "name": "Аллергический ринит",
                "probability": 0.10,
                "explanation": "Если есть связь с аллергенами"
            }
        ]
    elif "тошнота" in symptoms or "рвота" in symptoms:
        return [
            {
                "icd_code": "R11",
                "name": "Тошнота и рвота",
                "probability": 0.75,
                "explanation": "Симптомы желудочно-кишечного расстройства"
            },
            {
                "icd_code": "K29.7",
                "name": "Гастрит",
                "probability": 0.25,
                "explanation": "Воспаление слизистой желудка"
            }
        ]
    else:
        return [
            {
                "icd_code": "R69",
                "name": "Неуточненное заболевание",
                "probability": 1.0,
                "explanation": "Требуется дополнительное обследование"
            }
        ]

def generate_fallback_explanation(request: ExplanationRequest) -> str:
    """Генерирует объяснение, если ML API недоступно"""
    return (
        f"Диагноз {request.diagnosis_name} ({request.icd_code}) поставлен на основе симптомов: "
        f"'{request.symptoms}'. Для точного установления диагноза необходимо обратиться к врачу. "
        f"Данный диагноз является предположительным и требует подтверждения специалистом."
    )

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: SymptomRequest):
    """
    Принимает симптомы и возвращает диагнозы от ML API
    """
    try:
        if ML_API_AVAILABLE:
            print(f"🔍 Отправка симптомов в ML API: {request.symptoms}")
            diagnoses = ml_api.predict(request.symptoms)
            print(f"✅ Получен ответ от ML API: {len(diagnoses)} диагнозов")
        else:
            print(f"⚠️ ML API недоступно, используется заглушка")
            diagnoses = get_mock_diagnoses(request.symptoms)
        
        return {"diagnoses": diagnoses}
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return {
            "diagnoses": [{
                "icd_code": "R69",
                "name": "Ошибка обработки",
                "probability": 1.0,
                "explanation": f"Произошла ошибка: {str(e)}"
            }]
        }

@app.post("/explain", response_model=ExplanationResponse)
async def get_explanation(request: ExplanationRequest):
    """
    Возвращает подробное объяснение для конкретного диагноза
    """
    try:
        if ML_API_AVAILABLE:
            print(f"🔍 Запрос объяснения для: {request.icd_code}")
            
            # Отправляем запрос в ML API для получения объяснения
            # Предполагаем, что у ML API есть эндпоинт /explain
            response = ml_api.client.post(
                ml_api.api_url.replace("/predict", "/explain"),
                json={
                    "symptoms": request.symptoms,
                    "icd_code": request.icd_code,
                    "diagnosis_name": request.diagnosis_name
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result.get("explanation", "Объяснение недоступно")
            else:
                explanation = generate_fallback_explanation(request)
        else:
            explanation = generate_fallback_explanation(request)
        
        return {"explanation": explanation}
    
    except Exception as e:
        print(f"❌ Ошибка получения объяснения: {e}")
        return {"explanation": generate_fallback_explanation(request)}

@app.get("/health")
async def health_check():
    # Проверяем доступность ML API
    ml_api_status = "unknown"
    if ML_API_AVAILABLE:
        try:
            # Пробуем сделать тестовый запрос
            test_response = ml_api.client.get(ml_api.api_url.replace("/predict", "/health"))
            if test_response.status_code == 200:
                ml_api_status = "available"
            else:
                ml_api_status = "unavailable"
        except:
            ml_api_status = "unreachable"
    
    return {
        "status": "healthy",
        "ml_api": {
            "available": ML_API_AVAILABLE,
            "status": ml_api_status,
            "url": ml_api.api_url if ML_API_AVAILABLE else None
        },
        "message": "Server is running"
    }

# Создаем папку static если её нет
os.makedirs("static", exist_ok=True)

# Подключаем статические файлы
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("🚀 Сервер запускается...")
    print("📝 Откройте браузер: http://localhost:8001")
    print("🔧 Для остановки нажмите Ctrl+C")
    uvicorn.run(app, host="0.0.0.0", port=8001)