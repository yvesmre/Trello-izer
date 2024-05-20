import requests
import json
from variables import AUTH_TOKEN, API_KEY, FIT_OUT_BOARD
from import_myob_data import *
import pandas as pd
from styleframe import StyleFrame
import datetime

def import_cards_with_custom_fields_from_board(board):
  url = "https://api.trello.com/1/boards/" + board + "/cards"

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

  return json.loads(response.text)

def import_checklist(card):  
  url = "https://api.trello.com/1/cards/" + card + "/checklists/"

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
  }

  response = requests.request(
    "GET",
    url,
    params=query
  )

  return json.loads(response.text)

def import_cards_from_list(list):
  url = "https://api.trello.com/1/lists/" + list + "/cards"

  headers = {
    "Accept": "application/json"
  }

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
  )

  return json.loads(response.text)



def import_user(user):
  url = "https://api.trello.com/1/members/" + user

  headers = {
    "Accept": "application/json"
  }

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
  )

  return json.loads(response.text)

def import_card(card):
    url = "https://api.trello.com/1/cards/" + card

    headers = {
      "Accept": "application/json"
    }

    query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
    }

    response = requests.request(
      "GET",
      url,
      headers=headers,
      params=query
    )

    return json.loads(response.text)

def create_excel_file(board_id, filename):

  #Hacky way of going about this, tbh
  if not os.path.exists(os.getcwd() + "/" + filename.split('/')[1]) :
    os.makedirs(os.getcwd() + "/" + filename.split('/')[1])

  board = import_cards_with_custom_fields_from_board(board_id)

  to_json = {"Card Title": [], "Checklist": [], 'Checklist Item': [],  "Member": [] }

  user_to_name = {}
  for card in board:
    checklists = import_checklist(card['id'])

    card_name = card['name']
    
    for obj in checklists:
      for checklist_item in obj["checkItems"]:
        to_json['Card Title'].append(card_name)
        to_json['Checklist'].append(obj['name'])
        to_json['Checklist Item'].append(checklist_item['name'])
        if type(checklist_item['idMember']) is str:
          if checklist_item['idMember'] not in user_to_name.keys():
            user = import_user(checklist_item['idMember'])
            if 'fullName' in user:
              member = user['fullName']
              user_to_name[checklist_item['idMember']] = member
              to_json['Member'].append(member)
          else:
            to_json['Member'].append(user_to_name[checklist_item['idMember']])
        else: to_json['Member'].append('')

  frame = pd.DataFrame(data=to_json)


  writer = StyleFrame.ExcelWriter(os.getcwd() + filename)
  sf = StyleFrame(frame)
  # sf.P_FACTOR = 1
  # sf.A_FACTOR = 1

  sf.set_column_width(columns='Card Title', width=25)
  sf.set_column_width(columns='Checklist', width=50)
  sf.set_column_width(columns='Checklist Item', width=70)
  sf.set_column_width(columns='Member', width=25)
  sf.to_excel(excel_writer=writer, row_to_add_filters=0,index=False)


  writer.close()


create_excel_file(FIT_OUT_BOARD,  "/reports/" +  str(datetime.datetime.now()).replace(':','.') +  " fit out report.xlsx")
