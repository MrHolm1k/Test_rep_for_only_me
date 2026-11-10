import requests
import sys

urls = {'url_age': 'https://api.agify.io?', 'url_gen': 'https://api.genderize.io?'}
json_data = {'name': 'Маша'}

try:
    result_age = requests.get(urls['url_age'], params=json_data, timeout=10)
except requests.ConnectTimeout:
    sys.exit(1)

try:
    result_gen = requests.get(urls['url_gen'], params=json_data, timeout=10)
except requests.ConnectTimeout:
    sys.exit(1)


print(f"{json_data['name']}. Вероятный возраст {result_age.json()["age"]}.\nВероятность женского пола {result_gen.json()['probability']}.")
