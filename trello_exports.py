import requests
import json
import os
from variables import *


url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

initial_query = {
  'key': API_KEY,
  'token': AUTH_TOKEN,
}


def create_card(list, name, desc, template):
  query = dict(initial_query)
  query["name"] = name
  query["idList"] = list
  query["desc"] = desc
  query["idCardSource"] = template


  response = requests.request(
    "POST",
    url,
    headers=headers,
    params=query
  )
  JSON_Response = json.loads(response.text)
  
  return JSON_Response

def create_list(id, name, templateId):
  checklist_url = url + "/" + id + "/checklists"

  query = dict(initial_query)
  query["name"] = name
  query["idChecklistSource"] = templateId

  response = requests.request(
   "POST",
   checklist_url,
   params=query
  )

  return json.loads(response.text)

def update_card(card, desc):
  update_url = "https://api.trello.com/1/cards/" + card

  query = dict(initial_query)
  query['desc'] = desc

  response = requests.request(
    "PUT",
    update_url,
    headers=headers,
    params=query
  )

  return json.loads(response.text)

def create_attachment(card, link):
  attachment_url = "https://api.trello.com/1/cards/" + card + "/attachments"

  query = dict(initial_query)
  query["url"]= link

  response = requests.request(
    "POST",
    attachment_url,
    headers=headers,
    params=query
  )

  return json.loads(response.text)

##Testing
if __name__ == "__main__":
    create_list(create_card(TEST_LIST, 'Testing', "Test!", "")["id"], "Test Checklist", BUILD_CHECKLIST_TEMPLATE)
    