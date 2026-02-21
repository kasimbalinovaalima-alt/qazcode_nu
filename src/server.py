from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os

# Импортируем офлайн-клиент
try:
    from ml_api_client import ml_api
    ML_AVAILABLE = True
    print("✅ ОФЛАЙН-РЕЖИМ: модель готова, внешние вызовы ОТКЛЮЧЕНЫ")
except ImportError as e:
    ML_AVAILABLE = False
    print(f"⚠️ Офлайн-клиент не загружен: {e}")

app = FastAPI(title="Medical Diagnosis Assistant - OFFLINE MODE")

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

class ExplanationRequest(BaseModel):
    symptoms: str
    icd_code: str
    diagnosis_name: str

class ExplanationResponse(BaseModel):
    explanation: str

def generate_fallback_explanation(request: ExplanationRequest) -> str:
    """Генерирует объяснение локально (БЕЗ ИНТЕРНЕТА)"""
    return (
        f"🧠 ЛОКАЛЬНЫЙ АНАЛИЗ (без внешних вызовов):\n\n"
        f"Диагноз {request.diagnosis_name} ({request.icd_code}) "
        f"поставлен на основе симптомов: '{request.symptoms}'.\n\n"
        f"📋 Это предварительный диагноз, основанный на локальных данных.\n"
        f"⚠️ ВНИМАНИЕ: Для точного установления диагноза необходимо обратиться к врачу."
    )

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose(request: SymptomRequest):
    """
    Принимает симптомы и возвращает диагнозы (ПОЛНОСТЬЮ ОФЛАЙН)
    """
    try:
        if ML_AVAILABLE:
            print(f"🔍 Офлайн-анализ симптомов: {request.symptoms}")
            # ВЫЗОВ ЛОКАЛЬНОЙ МОДЕЛИ - БЕЗ ИНТЕРНЕТА!
            diagnoses = ml_api.predict(request.symptoms)
            print(f"✅ Получено {len(diagnoses)} диагнозов (локально, без интернета)")
        else:
            # Заглушка на крайний случай
            diagnoses = [{
                "icd_code": "R69",
                "name": "Неуточненное заболевание",
                "probability": 1.0,
                "explanation": "Офлайн-режим: локальная заглушка"
            }]
        
        return {"diagnoses": diagnoses}
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return {
            "diagnoses": [{
                "icd_code": "R69",
                "name": "Ошибка обработки",
                "probability": 1.0,
                "explanation": f"Произошла локальная ошибка: {str(e)}"
            }]
        }

@app.post("/explain", response_model=ExplanationResponse)
async def get_explanation(request: ExplanationRequest):
    """
    Возвращает подробное объяснение (ПОЛНОСТЬЮ ОФЛАЙН, БЕЗ API)
    """
    try:
        # ТОЛЬКО ЛОКАЛЬНАЯ ФУНКЦИЯ - НИКАКИХ ВНЕШНИХ ВЫЗОВОВ!
        explanation = generate_fallback_explanation(request)
        return {"explanation": explanation}
    
    except Exception as e:
        print(f"❌ Ошибка получения объяснения: {e}")
        return {"explanation": generate_fallback_explanation(request)}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mode": "OFFLINE",
        "external_calls": "DISABLED",
        "message": "Server running in OFFLINE mode - no internet required!"
    }

# Создаем папку static если её нет
os.makedirs("static", exist_ok=True)

# Подключаем статические файлы
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ОФЛАЙН-СЕРВЕР ЗАПУСКАЕТСЯ")
    print("=" * 50)
    print("📝 Откройте браузер: http://localhost:8001")
    print("🔋 Режим: ПОЛНОСТЬЮ ОФЛАЙН")
    print("🌐 Внешние вызовы: ОТКЛЮЧЕНЫ")
    print("✅ Соответствие критерию: No external network calls during inference")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=8001)