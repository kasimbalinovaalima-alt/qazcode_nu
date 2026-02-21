\### 1. структуру проекта

qazcode-nu/

├── src/

│ ├── server.py # Основной сервер (не трогать!)

│ ├── ml\_api\_client.py # Клиент для подключения к вашему API

│ └── ml\_model.py # СЮДА МОЖЕТЕ ВСТАВИТЬ ВАШУ МОДЕЛЬ

├── static/

│ └── index.html # Интерфейс (не трогать!)

└── data/

└── test\_set/ # Тестовые данные



ВАРИАНТ А - ЧЕРЕЗ ОТДЕЛЬНЫЙ API (РЕКОМЕНДУЕТСЯ)

Запустите свою модель как отдельный микросервис с тремя эндпоинтами:



\*\*POST /predict\*\*

\- Вход: `{"symptoms": "кашель, температура"}`

\- Выход: 

```json

\[

&nbsp; {

&nbsp;   "icd\_code": "J06.9",

&nbsp;   "name": "Острая инфекция",

&nbsp;   "probability": 0.85,

&nbsp;   "explanation": "Краткое объяснение"

&nbsp; }

]



**После запуска API нужно заменить URL, например:**

http://localhost:8002

http://192.168.1.100:8000

http://ml-container:8000



Мы изменим одну строку в src/ml\_api\_client.py: 

ml\_api = MLModelAPIClient(api\_url="http://ВАШ\_АДРЕС:ПОРТ/predict")





Модель должна возвращать список словарей:

\[

&nbsp;   {

&nbsp;       "icd\_code": "J06.9",        # строка, код МКБ-10

&nbsp;       "name": "Название диагноза", # строка

&nbsp;       "probability": 0.85,         # число от 0 до 1

&nbsp;       "explanation": "Объяснение"  # строка

&nbsp;   }

]

Запустите сервер:

python src/server.py 



Откройте браузер: http://localhost:8001

