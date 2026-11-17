import http_classes_methods
import parcer_classes
import myException 
import sys


urls = {
    'url_age': 'https://api.agify.io?',
    'url_gen': 'https://api.genderize.io?', 
    'param_url': 'https://jsonplaceholder.typicode.com/posts'
}


if __name__ == "__main__":
    try:
        name_param = input('Введите имя: ')
    except myException.InvalidInput as e:
        print(e)
        sys.exit()
