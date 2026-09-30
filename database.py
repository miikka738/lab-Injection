import os
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_db_connection() -> Optional[psycopg2.extensions.connection]:

    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None

def init_db() -> None:

    conn = get_db_connection()
    if not conn:
        print("Не удалось подключиться к базе данных.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50)
                );
            """)

            users_data = [
                ("admin", "admin_pass", "Иван", "Иванов"),
                ("guest", "guest123", "Гость", "Тестовый"),
                ("manager", "manager123", "Петр", "Менеджер")
            ]

            for username, password, first_name, last_name in users_data:
                cur.execute("""
                    INSERT INTO users (username, password, first_name, last_name)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (username) DO NOTHING;
                """, (username, password, first_name, last_name))

        conn.commit()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        conn.rollback()
    finally:
        conn.close()