import requests

BASE_URL = "http://127.0.0.1:5000/"

get_r = requests.get(BASE_URL)
print(get_r.status_code)
print(get_r.text)

post_r = requests.post(BASE_URL)
print(post_r.status_code)
print(post_r.text)