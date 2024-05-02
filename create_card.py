import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


auth_token = os.getenv("AUTH_TOKEN")
api_key = os.getenv("API_KEY")

headers = {
  "Accept": "application/json"
}

query = {
  'key': api_key,
  'token': auth_token,
}


def create_card(list, name, desc):
  queryCopy = dict(query)
  queryCopy["name"] = name
  queryCopy["idList"] = list
  queryCopy["desc"] = desc

  url = "https://api.trello.com/1/cards"

  response = requests.request(
    "POST",
    url,
    headers=headers,
    params=queryCopy
  )
  JSON_Response = json.loads(response.text)
  
  return JSON_Response

def create_list(id, name, templateId):
  url = "https://api.trello.com/1/cards/" + id + "/checklists"

  queryCopy = dict(query)
  queryCopy["name"] = name
  queryCopy["idChecklistSource"] = templateId

  response = requests.request(
   "POST",
   url,
   params=queryCopy
  )

  return json.loads(response.text)

  print(response.text)




##Testing
if __name__ == "__main__":
    BUILD_CHECKLIST = os.getenv("BUILD_CHECKLIST")
    TEST_LIST = os.getenv("TEST_LIST")
    create_list(create_card(TEST_LIST, 'Testing', "Test!")["id"], "Test Checklist", BUILD_CHECKLIST)
    