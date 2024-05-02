import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()



auth_token = os.getenv("AUTH_TOKEN")
api_key = os.getenv("API_KEY")
PRODUCTION_BOARD = os.getenv("PRODUCTION_BOARD")

url = "https://api.trello.com/1/boards/" + PRODUCTION_BOARD + "/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'key': api_key,
  'token': auth_token,
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