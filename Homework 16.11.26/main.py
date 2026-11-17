import http_classes_methods
import parcer_classes
import myException 
import sys

EXIT_CODE_INVALID_INPUT = 1



urls = {
    'url_age': 'https://api.agify.io?',
    'url_gen': 'https://api.genderize.io?', 
    'param_url': 'https://jsonplaceholder.typicode.com/posts',
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) СекретныйАгентБот/1.0",
    "Accept-Language": "ru-RU,ru;q=0.9",
}

# Невалидный json ловить перед тем как вообще отправлять в клиент

if __name__ == "__main__":
    try:
        name_param = input('Введите имя: ').strip()

    except myException.InvalidInput as e:
        print(e)
        sys.exit(EXIT_CODE_INVALID_INPUT)
    
    
