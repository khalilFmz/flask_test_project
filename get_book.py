import requests
import json

url = 'http://127.0.0.1:5000/get'

print('entered the loop')
r = requests.get(url = url, params = {'book_id' : 3})
print(r.text)

