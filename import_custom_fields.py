import requests
import json
from variables import AUTH_TOKEN, API_KEY, FIT_OUT_BOARD

url = "https://api.trello.com/1/boards/" + FIT_OUT_BOARD + "/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'key': API_KEY,
  'token': AUTH_TOKEN,
  "customFieldItems":"true"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
)


# print(response.text)
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))