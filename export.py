import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


auth_token = os.getenv("AUTH_TOKEN")
api_key = os.getenv("API_KEY")

list = "6632e70f9c08b15bc441c7cf"

url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'idList': list,
  'key': api_key,
  'token': auth_token,
  'name': "Test Me!"
}

response = requests.request(
   "POST",
   url,
   headers=headers,
   params=query
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))