import requests
import json
import csv
import pandas as pd
from variables import AUTH_TOKEN, API_KEY, PRODUCTION_BOARD


lists_request_url = "https://api.trello.com/1/boards/IdICNLK4/lists"

headers = {
  "Accept": "application/json"
}

query = {
  'key': API_KEY,
  'token': AUTH_TOKEN
}

response = requests.request(
   "GET",
   lists_request_url,
   headers=headers,
   params=query
)


JSON_response = json.loads(response.text)



list_and_cards_dict = {}

for obj in JSON_response:
    list_and_cards_dict[obj["id"]] = []

for key in list_and_cards_dict.keys(): 
  card_request_url = "https://api.trello.com/1/lists/" + key + "/cards"
  response = requests.request(
    "GET",
    card_request_url,
    headers=headers,
    params=query
  )

  JSON = json.loads(response.text)

  for obj in JSON:
     list_and_cards_dict[key].append(obj["id"])

  list_and_cards_dict[key].reverse()


def isEmpty(lists_):
  for list in lists_:
    if len(list) > 0:
        return False
      
  return True


listCopy = dict(list_and_cards_dict)



with open('test.csv', 'w', newline='') as csvfile:
    fieldnames = list_and_cards_dict.keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    while not isEmpty(list_and_cards_dict.values()):
      to_write = {}
      for key, values in listCopy.items():
         to_write[key] = values.pop() if len(values) > 0 else ''
      writer.writerow(to_write)

