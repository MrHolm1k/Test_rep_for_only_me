import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass

from myException import HttpRequestError
from json import JSONDecodeError

EXIT_CODE_TIMEOUT = 2
EXIT_CODE_HTTPERROR = 3


# kw_only чтобы нельзя было передовать по порядку, а чётко указывать, что какому параметру передаём
@dataclass(frozen=True, kw_only=True)
class HttpRequest:
    url: str 
    timeout: int = 10
    headers: dict[str, str] | None = None
    params: dict | None = None
    json_data: dict | None = None



# Классы для запросов HTTP

class GetMethod(ABC):
    @abstractmethod
    def get_method(self) -> str:
        ...

class HTTPmethods(GetMethod, ABC):
    @abstractmethod
    def http_request(self, session: requests.Session, request_data: HttpRequest) -> requests.Response:
        ...

class GetHttpMethod(HTTPmethods):
    def http_request(self, session: requests.Session, request_data: HttpRequest) -> requests.Response:
        return session.get(request_data.url, params=request_data.params,
                           headers=request_data.headers, timeout=request_data.timeout)
    
    def get_method(self) -> str:
        return f"HTTP GET METHOD"

class PostHttpMethod(HTTPmethods):
    def http_request(self, session: requests.Session, request_data: HttpRequest) -> requests.Response:
        return session.post(request_data.url, json=request_data.json_data,
                           headers=request_data.headers, timeout=request_data.timeout)

    def get_method(self) -> str:
        return f"HTTP POST METHOD"

# HTTP клиенты классы
class HttpClient(ABC):
    @abstractmethod
    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest) -> dict | str | list:
        ...
    
    
class RequestsHttpClient(HttpClient):
    def __init__(self, session: requests.Session | None = None):
        #  или self._session = session or requests.Session()
        if not session == None:
            self._session = session # protectid поле
        elif session == None: 
            self._session = requests.Session()

    # Крайне ограниченная функция, надо добавить, что возращать: json, str, code, headers и т.д.
    # Чтобы этого избежать лушче создать data_class со всеми необходимыми данными

    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest) -> dict | str | list:
        try:
            response: requests.Response = method.http_request(self._session, request_data)
            response.raise_for_status()

        # Слишком долго сервер не отвечает
        except requests.exceptions.Timeout as error:
            raise HttpRequestError(
                exit_code=EXIT_CODE_TIMEOUT,
                message=f"{method.get_method()}: нет ответа от {request_data.url} "
                f"за {request_data.timeout} секунд"
            ) from error # Нужен для того чтобы показывал всю цепочку вызываемых ошибок

        # Если выкинет 4xx или 5xx ошибки
        except requests.exceptions.HTTPError as error:
            failed_response = error.response
            status_code = failed_response.status_code if failed_response is not None else None
            message = f"{method.get_method()}: {request_data.url} — {error}"
            # Сам сервер может что-нибудь кинуть сообщение, но это на потом реализацию оставлю
            raise HttpRequestError(exit_code=EXIT_CODE_HTTPERROR, message=message, status_code=status_code) from error

        except requests.exceptions.RequestException as error:
            raise HttpRequestError(
                message=f"{method.get_method()}: сбой соединения с {request_data.url} — {error}"
            ) from error

        # Конец блока с ошибками от сервера
        try:
            if "json" in response.headers.get("Content-Type", ""):
                temp: list | dict = response.json() 
                return temp
        except ValueError:
            pass

        return response.text
