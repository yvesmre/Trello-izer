import requests
import json
import os
from dotenv import load_dotenv
import csv
import pandas as pd

load_dotenv()


auth_token = os.getenv("AUTH_TOKEN")
api_key = os.getenv("API_KEY")
PRODUCTION_BOARD = os.getenv("PRODUCTION_BOARD")

lists_request_url = "https://api.trello.com/1/boards/" + PRODUCTION_BOARD + "/cards"

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
   lists_request_url,
   headers=headers,
   params=query
)


JSON_response = json.loads(response.text)

print(json.dumps(JSON_response, sort_keys=True, indent=4, separators=(",", ": ")))

pd.read_json(json.dumps(JSON_response, sort_keys=True, indent=4, separators=(",", ": "))).to_json("cards.json", indent = 4)

CSV = pd.read_json(response.text).to_csv("cards.csv")

JSON = pd.read_csv("cards.csv").to_json()

print(JSON)
