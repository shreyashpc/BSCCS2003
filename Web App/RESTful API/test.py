import requests

BASE_URL = "http://127.0.0.1:5000/"

# get_r = requests.get(BASE_URL + "api/shreyash")
# print(get_r.status_code)
# print(get_r.text)
# print(get_r.headers)

post_r = requests.post(BASE_URL+"api/Shreyash", {'name': 'Shreyash', 'roll_no': 'abc', 'country': 'India'})
print(post_r.status_code)
print(post_r.text)