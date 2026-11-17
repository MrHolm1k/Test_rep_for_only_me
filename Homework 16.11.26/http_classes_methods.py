import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import JSONDecodeError

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
    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest) -> dict | str:
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

    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest):
        try:
            response: requests.Response = method.http_request(self._session, request_data)
            response.raise_for_status()
        except requests.HTTPError as e:
            raise
        except requests.RequestException as e: 
            raise        
        try:
            if "json" in response.headers.get("Content-Type", ""):
                return response.json()
        except JSONDecodeError:
            pass

        return response.text
