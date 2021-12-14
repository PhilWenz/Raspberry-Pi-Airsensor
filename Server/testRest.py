import requests
import json
url = 'http://127.0.0.1:5000/'
payload = {'start_date': "2021-09-06T17:50:58.798975",
           'end_date': "2021-09-06T20:52:58.798975",
           'last': True}


headers = {"content-type": "application/json"}

r = requests.get(url, data=json.dumps(payload), headers=headers)

print(r)
print(r.json())