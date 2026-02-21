
Medical Diagnosis Assistant 

##Система, которая по тексту симптомов возвращает:
- Топ-3 вероятных диагноза с ICD-10 кодами
- Процент вероятности для каждого диагноза
- Подробное объяснение на основе клинических протоколов Казахстана

## Быстрый старт

Способ 1: Запуск через Python (локально)
```bash
# 1. Клонировать репозиторий
git clone https://github.com/kasimbalinovaalima-alt/qazcode_nu.git
cd qazcode_nu
# 2. Установить зависимости
pip install fastapi uvicorn httpx
# 3. Запустить сервер
python src/server.py
# 4. Открыть в браузере
http://localhost:8001

Способ 2:
# 1. Собрать образ
docker build -t medical-diagnosis .
# 2. Запустить контейнер
docker run -p 8080:8001 medical-diagnosis
# 3. Открыть в браузере
http://localhost:8080