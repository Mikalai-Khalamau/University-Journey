import psycopg
from psycopg.rows import dict_row
from app.config import settings

def get_db():
    # Подключаемся и настраиваем возврат строк как словарей
    conn = psycopg.connect(settings.DATABASE_URL, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()