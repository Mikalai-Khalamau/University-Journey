import psycopg
from datetime import datetime, timedelta
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.config import settings

def generate_test_data():
    print("🔌 Подключение к базе данных...")
    conn = psycopg.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cur = conn.cursor()

    try:
        # 1. Линии
        print(" Добавляем линии...")
        new_lines = [('Серебрянка', 'серебряный', 4), ('Лошицкая', 'желтый', 5)]
        for line in new_lines:
            cur.execute("INSERT INTO lines (name, color, number) VALUES (%s, %s, %s) ON CONFLICT (number) DO NOTHING",
                        line)

        cur.execute("SELECT id FROM lines WHERE name IN ('Серебрянка', 'Лошицкая')")
        line_ids = [row[0] for row in cur.fetchall()]
        if not line_ids:
            print("Линии уже существуют, пропускаем")
            return

        # 2. Станции
        print("➕ Добавляем станции...")
        new_stations = [
            (line_ids[0], 'Серебрянка-1', 12, True),
            (line_ids[0], 'Серебрянка-2', 15, False),
            (line_ids[0], 'Серебрянка-3', 8, True),
            (line_ids[1], 'Лошица-1', 10, True),
            (line_ids[1], 'Лошица-2', 14, False),
            (line_ids[1], 'Лошица-3', 11, True)
        ]
        for station in new_stations:
            cur.execute("INSERT INTO stations (line_id, name, depth, has_escalator) VALUES (%s, %s, %s, %s)", station)

        cur.execute("SELECT id FROM stations WHERE name LIKE 'Серебрянка%' OR name LIKE 'Лошица%'")
        station_ids = [row[0] for row in cur.fetchall()]

        # 3. Поезда
        print(" Добавляем поезда...")
        new_trains = [
            (line_ids[0], '4001', 'Минск-2024', 'line'),
            (line_ids[0], '4002', 'Минск-2024', 'depo'),
            (line_ids[1], '5001', 'Олег', 'line'),
            (line_ids[1], '5002', 'Олег', 'renovation')
        ]
        for train in new_trains:
            cur.execute(
                "INSERT INTO trains (line_id, number, model, status) VALUES (%s, %s, %s, %s) ON CONFLICT (number) DO NOTHING",
                train)

        cur.execute("SELECT id FROM trains WHERE number IN ('4001', '4002', '5001', '5002')")
        train_ids = [row[0] for row in cur.fetchall()]

        # 4. Оборудование
        print("➕ Добавляем оборудование...")
        equipment_types = [('турникет', 'Турникет входной'), ('эскалатор', 'Эскалатор наклонный'),
                           ('вентилятор', 'Вентилятор шахтный')]
        for st_id in station_ids[:4]:
            for eq_type, eq_name in equipment_types:
                cur.execute("INSERT INTO equipment (station_id, type, name, status) VALUES (%s, %s, %s, 'ok')",
                            (st_id, eq_type, f"{eq_name} {st_id}"))

        # 5. Пассажиры и проездные
        print("➕ Добавляем пассажиров и проездные...")
        new_passengers = [
            ('Козлов Дмитрий', '+375291112233', 'kozlov@mail.ru'),
            ('Новик Анна', '+375294445566', 'novik@mail.ru'),
            ('Жук Петр', '+375297778899', 'zhuk@mail.ru'),
            ('Мороз Елена', '+375290001122', 'moroz@mail.ru'),
            ('Волк Сергей', '+375293334455', 'volk@mail.ru')
        ]
        passenger_ids = []
        for p in new_passengers:
            cur.execute("INSERT INTO passengers (full_name, phone, email) VALUES (%s, %s, %s) RETURNING id", p)
            passenger_ids.append(cur.fetchone()[0])

        pass_types = ['month', 'day', 'decade']
        for p_id in passenger_ids:
            p_type = random.choice(pass_types)
            balance = random.randint(1, 30)
            exp_date = datetime.now() + timedelta(days=random.randint(10, 60))
            cur.execute("INSERT INTO passes (passenger_id, type, balance, expiration_date) VALUES (%s, %s, %s, %s)",
                        (p_id, p_type, balance, exp_date.date()))

        # 6. Рейсы
        print("➕ Генерируем рейсы...")
        base_date = datetime(2024, 1, 15, 8, 0)
        for i in range(500):
            train_id = random.choice(train_ids) if train_ids else 1
            station_id = random.choice(station_ids) if station_ids else 1
            departure = base_date + timedelta(minutes=i * 10)
            arrival = departure + timedelta(minutes=15)
            status = random.choice(['on schedule', 'on schedule', 'on schedule', 'delayed'])

            cur.execute("""
                INSERT INTO trips (train_id, station_id, departure_time, arrival_time, trip_date, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (train_id, station_id, departure.time(), arrival.time(), departure.date(), status))

        conn.commit()
        print("✅ Тестовые данные успешно добавлены!")

    except Exception as e:
        print(f" Ошибка: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    generate_test_data()