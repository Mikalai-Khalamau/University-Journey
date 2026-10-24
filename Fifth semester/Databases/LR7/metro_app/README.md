## Установка и запуск

### 1. Запуск базы данных (Docker)
Убедитесь, что Docker установлен и запущен. В корневой директории выполните:
docker-compose up -d

База данных PostgreSQL будет доступна на localhost:5432

### 2. Настройка окружения Python
Создайте виртуальное окружение и установите зависимости:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

### 3. Инициализация базы данных
Подключитесь к базе данных через DBeaver и выполните SQL-скрипт создания таблиц 
Параметры подключения:
- Host: localhost
- Port: 5432
- Database: postgres
- User: postgres
- Password: postgres

### 4. Генерация тестовых данных
Для наполнения базы данных тестовыми записями выполните скрипт:
python generate_data.py

### 5. Запуск API сервера
uvicorn main:app --reload

После запуска сервера интерактивная документация Swagger UI будет доступна по адресу:
http://127.0.0.1:8000/docs

В Swagger UI вы можете протестировать все эндпоинты
