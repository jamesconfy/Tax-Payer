import requests

BASE = "http://127.0.0.1:5000/accountant"

response = requests.get(BASE)
print(response.json())