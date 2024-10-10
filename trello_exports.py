import requests
import json
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

  return json.loads(response.text)

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

def delete_list(id, checklist_id):
  checklist_url = url + "/" + id + "/checklists/" + checklist_id

  query = dict(initial_query)

  response = requests.request(
   "DELETE",
   checklist_url,
   params=query
  )

  return json.loads(response.text)


def delete_list_item(checklist_id, checkitem_id):

  url = "https://api.trello.com/1/checklists/" + checklist_id + "/checkItems/" + checkitem_id

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN
  }

  response = requests.request(
    "DELETE",
    url,
    params=query
  )

  return json.loads(response.text)


def create_list_item(checklist_id, name, checked, pos):
  url = "https://api.trello.com/1/checklists/" + checklist_id + "/checkItems"

  query = {
    'name':  name,
    'checked': 'true' if checked else 'false',
    'pos': pos,
    'key': API_KEY,
    'token': AUTH_TOKEN
  }

  response = requests.request(
    "POST",
    url,
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



def delete_card(card):
  url = "https://api.trello.com/1/cards/" + card

  query = initial_query

  response = requests.request(
    "DELETE",
    url,
    params=query
  )

  return response.text



def delete_attachment(card, attachment):
  url = "https://api.trello.com/1/cards/" + card + "/attachments/" + attachment

  query = initial_query
  
  response = requests.request(
    "DELETE",
    url,
    params=query
  )

  return (response.text)

##Testing
if __name__ == "__main__":
    create_list(create_card(TEST_LIST, 'Testing', "Test!", "")["id"], "Test Checklist", BUILD_CHECKLIST_TEMPLATE)
    