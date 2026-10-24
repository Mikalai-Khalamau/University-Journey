# Лабораторная работа по ООП. 
# Реализация серверной части системы доставки еды с применением архитектурного паттерна Clean Architecture.

# 1. Создать виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить сервер
uvicorn main:app --reload

# 4. Открыть Swagger-документацию
# http://127.0.0.1:8000/docs

# Запустить все тесты
pytest -v

# Запустить с покрытием
pytest --cov=. --cov-report=html