import logging
from fastapi import FastAPI, Query
from database import get_db_connection
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

@app.get("/vulnerabilities/sqli/")
async def sqli_vulnerability(
        username: str,
        password: str,
        user_token: Optional[str] = None,
        Login: Optional[str] = None
):

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        if not conn:
            return {"status": "error", "message": "Database connection failed"}

        cursor = conn.cursor()

        query = "SELECT first_name, last_name FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:
            logging.info(f"Успешный вход пользователя: {username}")
            return {
                "status": "success",
                "data": {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
                }
            }
        else:
            logging.warning(f"Неудачная попытка входа для: {username}")
            return {
                "status": "error",
                "message": "User not found"
            }

    except Exception as e:
        logging.error(f"Database error: {e}")
        return {
            "status": "error",
            "message": "Internal server error"
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()