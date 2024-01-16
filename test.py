import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "test3")
# print(response.json())

response = requests.post(BASE + "test4", {'filename': "result.json"})
print(response)
