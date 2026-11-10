import requests



# status_code - код http
# text - получение ссобщения на сайте
# json - получения json
# url - получение ссылки

# Can params=dict() in method get
# get - get somthing from
# post - send somthing json or data

url = 'https://httpbin.org/post'

payload_form = {'username': 'admin', 'password':'secret'}

respons = requests.post(url, data=payload_form)

print(respons.text)

