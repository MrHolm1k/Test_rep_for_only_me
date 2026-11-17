import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class HttpRequest:
    url: str 
    timeout: int = 10
    headers: dict[str, str] | None = None
    params: dict | None = None
    json_data: dict | None = None


class GetMethod(ABC):
    @abstractmethod
    def get_method(self) -> str:
        ...

class HTTPmethods(GetMethod, ABC):
    @abstractmethod
    def http_request(self, session: requests.Session, request_data: HttpRequest) -> requests.Response:
        ...


class HttpClient(ABC):
    @abstractmethod
    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest):
        ...
    
    
class ReqestsHttpClient(HttpClient):
    def __init__(self, session: requests.Session | None):
        if not session == None:
            self._session = session # protectid поле
        else: 
            self._session = requests.Session()

    # Крайне ограниченная функция, надо добавить, что возращать: json, str, code, headers и т.д.
    # Умышленно убрал, что функция должна возращать

    def send_http_request(self, method: HTTPmethods, request_data: HttpRequest):
        try:
            response: requests.Response = method.http_request(self._session, request_data)
            response.raise_for_status()
        except requests.RequestException as e: 
            print(f"")
            raise 
        except

        if "json" in response.headers["Content-Type"]:
            return response.json()
        


# try:
#     result_age = requests.get(urls['url_age'], params=json_data, timeout=10)
# except requests.ConnectTimeout:
#     sys.exit(1)
#
# try:
#     result_gen = requests.get(urls['url_gen'], params=json_data, timeout=10)
# except requests.ConnectTimeout:
#     sys.exit(1)
#
# print(f"{json_data['name']}. Вероятный возраст {result_age.json()["age"]}.\nВероятность женского пола {result_gen.json()['probability']}.")


