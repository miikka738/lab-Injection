import html

def render_form() -> str:
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head><meta charset="utf-8"><title>Форма авторизации</title></head>
    <body>
      <h3>Вход в систему</h3>
      <form action="/vulnerabilities/sqli/" method="GET">
        <label>Username: <input type="text" name="username" required></label><br><br>
        <label>Password: <input type="password" name="password" required></label><br><br>
        <label>User Token: <input type="text" name="user_token" value="test_token" required></label><br><br>
        <label>Login: <input type="text" name="Login" value="Login" required></label><br><br>
        <button type="submit">Submit</button>
      </form>
    </body>
    </html>
    """

def render_success(username: str, first_name: str, last_name: str) -> str:

    escaped_username = html.escape(username)
    escaped_first_name = html.escape(first_name)
    escaped_last_name = html.escape(last_name)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Успешный вход</title>
    </head>
    <body>
        <h1>Добро пожаловать, {escaped_username}!</h1>
        <p>Имя: {escaped_first_name}</p>
        <p>Фамилия: {escaped_last_name}</p>
    </body>
    </html>
    """


def render_error(message: str) -> str:

    escaped_message = html.escape(message)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ошибка</title>
    </head>
    <body>
        <h1>Ошибка</h1>
        <p>{escaped_message}</p>
    </body>
    </html>
    """