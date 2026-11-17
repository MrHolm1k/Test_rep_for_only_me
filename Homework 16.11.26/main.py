import requests
import http_classes_methods
import parcer_classes
import myException 
import sys

EXIT_CODE_INVALID_INPUT = 1

# Мой номер 20, но колличество userId только 10, поэтому введу 2
userId = 2

urls_get = {
    'url_age': 'https://api.agify.io',
    'url_gen': 'https://api.genderize.io', 
}

urls_post = {
    'param_url': 'https://jsonplaceholder.typicode.com/posts',
    'post_bin': 'https://httpbin.org/post',
}

url_download = {
    'random_img': 'https://picsum.photos/400/300',
}

# Другие заголовки допишуться самостоятельно. Кстати их можно либо сделать как ссесия либо вручную передовать, очень удобно сделано у меня
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SecreteAgent/1.0",
    "Accept-Language": "ru-RU,ru;q=0.9",
}

# Невалидный json ловить перед тем как вообще отправлять в клиент

if __name__ == "__main__":
    client = http_classes_methods.RequestsHttpClient()
    try:
        name_param = input('Введите имя: ').strip()
        if name_param == "":
            raise myException.InvalidInput("Пустая строка")
        elif len(name_param.split()) > 1:
            raise myException.InvalidInput("Переданно больше одного имени")
        params_1 = {"name": name_param}
    except myException.InvalidInput as e:
        print(e)
        sys.exit(EXIT_CODE_INVALID_INPUT)
    
    # Тут лежат результаты get запросов
    get_client_result = dict()
    for url in urls_get.values():
        data = http_classes_methods.HttpRequest(
            url=url,
            params=params_1,
            headers=headers, 
            timeout=3,
        )
        
        try:
            get_client_result[url] = client.send_http_request(http_classes_methods.GetHttpMethod(), data)
        except myException.HttpRequestError as e:
            print(f"Текст ошибки: {e.message}")
            if not e.status_code == None:
                print(f"Http код: {e.status_code}")
            cause_of_exception = type(e.__cause__).__name__
            print(f"Причина {cause_of_exception}")
            sys.exit(e.exit_code)

    print(f"Цель: {name_param}. Вероятный возраст: {get_client_result[urls_get['url_age']]["age"]}. Вероятность женского пола: {get_client_result[urls_get['url_gen']]['probability'] * 100}%.")
    # Для задержки
    input("Задержка")
    
    # Делаем третий get запрос
    params_2 = {"userId": userId}
    data = http_classes_methods.HttpRequest(
        url=urls_post['param_url'],
        params=params_2,
        headers=headers,
        timeout=3,
    )
    try:
        json_result = client.send_http_request(http_classes_methods.GetHttpMethod(), data)
    except myException.HttpRequestError as e:
        print(f"Текст ошибки: {e.message}")
        if not e.status_code == None:
            print(f"Http код: {e.status_code}")
        cause_of_exception = type(e.__cause__).__name__
        print(f"Причина {cause_of_exception}")
        sys.exit(e.exit_code)
    
    print(f"Длинна {len(json_result)}, первый заголовок {json_result[0]["title"]}")
    input("Задержка")
    
    # Делаем post запрос 
    json_data = {
        "name": name_param, 
        "age": get_client_result[urls_get['url_age']]["age"],
        "amount_of_posts": len(json_result)
    }
    data = http_classes_methods.HttpRequest(
        url=urls_post['post_bin'],
        json_data=json_data,
        headers=headers,
        timeout=3,
    )
    try:
        result = client.send_http_request(http_classes_methods.PostHttpMethod(), data)
    except myException.HttpRequestError as e:
        print(f"Текст ошибки: {e.message}")
        if not e.status_code == None:
            print(f"Http код: {e.status_code}")
        cause_of_exception = type(e.__cause__).__name__
        print(f"Причина {cause_of_exception}")
        sys.exit(e.exit_code)

    if isinstance(result["json"],dict): 
        print(f"Сервер принял как json")
    else:
        print(f"Сервер не принял как json")

    input("Задержка")
    # Надо будет написать класс потом в клиенте для скачивания http 
    with requests.get(url_download["random_img"], stream=True, timeout=3) as r:
        with open("evidence.jpg", "wb") as img: 
            for part in r.iter_content(chunk_size=8000):
                img.write(part)




    


    

    


    
    
        
        

        



    
    
