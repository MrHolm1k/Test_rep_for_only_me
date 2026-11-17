class InvalidInput(Exception):
    def __init__(self, massage: str = "Невалидная запись"):
        super().__init__(massage)


class HttpRequestError(Exception):
    """Ошибка HTTP-запроса: таймаут, 4xx/5xx или сбой соединения.

    status_code равен None, если ответ от сервера так и не пришёл
    (например, при таймауте).
    """

    def __init__(self, exit_code: int=1000,  message: str = "Ошибка HTTP-запроса", status_code: int | None = None):
        self.exit_code = exit_code
        self.message = message
        self.status_code = status_code
        text = f"HTTP {status_code}: {message}" if status_code is not None else message
        super().__init__(text)
