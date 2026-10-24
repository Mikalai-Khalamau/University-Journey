"""initial schema

Revision ID: initial
Revises:
Create Date: 2024-10-12 12:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Выполняем наш SQL-скрипт создания таблиц
    op.execute("""
        CREATE TABLE lines (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            color VARCHAR(20) NOT NULL,
            number INT NOT NULL UNIQUE
        );

        CREATE TABLE passengers (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(200) NOT NULL,
            phone VARCHAR(20),
            email VARCHAR(100)
        );

        CREATE TABLE system_users (
            id SERIAL PRIMARY KEY,
            login VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'admin')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE stations (
            id SERIAL PRIMARY KEY,
            line_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            depth INT,
            has_escalator BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (line_id) REFERENCES lines(id) ON DELETE CASCADE
        );

        CREATE TABLE trains (
            id SERIAL PRIMARY KEY,
            line_id INT NOT NULL,
            number VARCHAR(20) NOT NULL UNIQUE,
            model VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'depo' CHECK (status IN ('line', 'depo', 'renovation')),
            FOREIGN KEY (line_id) REFERENCES lines(id) ON DELETE CASCADE
        );

        CREATE TABLE equipment (
            id SERIAL PRIMARY KEY,
            station_id INT NOT NULL,
            type VARCHAR(50) NOT NULL,
            name VARCHAR(100) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'ok' CHECK (status IN ('ok', 'broke', 'renovation')),
            FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
        );

        CREATE TABLE trips (
            id SERIAL PRIMARY KEY,
            train_id INT NOT NULL,
            station_id INT NOT NULL,
            departure_time TIME NOT NULL,
            arrival_time TIME NOT NULL,
            trip_date DATE NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'on schedule' CHECK (status IN ('on schedule', 'delayed', 'cancelled')),
            FOREIGN KEY (train_id) REFERENCES trains(id) ON DELETE CASCADE,
            FOREIGN KEY (station_id) REFERENCES stations(id) ON DELETE CASCADE
        );

        CREATE TABLE passes (
            id SERIAL PRIMARY KEY,
            passenger_id INT NOT NULL,
            type VARCHAR(50) NOT NULL CHECK (type IN ('day', 'month', 'decade')),
            balance INT NOT NULL DEFAULT 0,
            expiration_date DATE NOT NULL,
            FOREIGN KEY (passenger_id) REFERENCES passengers(id) ON DELETE CASCADE
        );

        CREATE TABLE incidents (
            id SERIAL PRIMARY KEY,
            equipment_id INT NOT NULL,
            reported_id INT NOT NULL,
            description TEXT,
            status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'work', 'fixed')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
            FOREIGN KEY (reported_id) REFERENCES system_users(id) ON DELETE CASCADE
        );

        CREATE TABLE action_logs (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL,
            action_type VARCHAR(50) NOT NULL CHECK (action_type IN ('insert', 'update', 'delete', 'login')),
            entity_name VARCHAR(50) NOT NULL,
            entity_id INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES system_users(id) ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
    # Откатываем изменения (удаляем таблицы в обратном порядке из-за внешних ключей)
    op.execute("""
        DROP TABLE IF EXISTS action_logs CASCADE;
        DROP TABLE IF EXISTS incidents CASCADE;
        DROP TABLE IF EXISTS passes CASCADE;
        DROP TABLE IF EXISTS trips CASCADE;
        DROP TABLE IF EXISTS equipment CASCADE;
        DROP TABLE IF EXISTS trains CASCADE;
        DROP TABLE IF EXISTS stations CASCADE;
        DROP TABLE IF EXISTS lines CASCADE;
        DROP TABLE IF EXISTS passengers CASCADE;
        DROP TABLE IF EXISTS system_users CASCADE;
    """)