import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from database import get_db_connection
from typing import Optional
from views import render_success, render_error, render_form

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return render_form()

@app.get("/vulnerabilities/sqli/", response_class=HTMLResponse)
async def sqli_vulnerability(
        username: str,
        password: str,
        user_token: Optional[str] = None,
        Login: Optional[str] = None
):

    if not user_token or not Login:
        return HTMLResponse(
            content=render_error("Missing required parameters: user_token or Login"),
            status_code=400
        )

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        if not conn:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cursor = conn.cursor()

        query = "SELECT first_name, last_name FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:
            logging.info(f"Успешный вход пользователя: {username}")
            return HTMLResponse(
                content=render_success(username, user["first_name"], user["last_name"]),
                status_code=200
            )
        else:
            logging.warning(f"Неудачная попытка входа для: {username}")
            return HTMLResponse(
                content=render_error("User not found"),
                status_code=404
            )

    except Exception as e:
        logging.error(f"Database error: {e}")
        return HTMLResponse(
            content=render_error("Internal server error"),
            status_code=500
        )

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)