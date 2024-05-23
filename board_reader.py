import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd
from variables import *
import emailer
import schedule
import time
import gc

headers = {
  "Accept": "application/json"
}

def get_cards(board):

  board_url = "https://api.trello.com/1/boards/" + board + "/cards"

  query = {
    'key': API_KEY,
    'token': AUTH_TOKEN,
    "customFieldItems":"true"
  }

  response = requests.request(
    "GET",
    board_url,
    headers=headers,
    params=query
  )


  JSON_response = json.loads(response.text)

  return json.dumps(JSON_response, sort_keys=True, indent=4, separators=(",", ": "))

  


def look_for_duplicates(board, name):
    
  url = "https://api.trello.com/1/boards/" + board + "/cards"

  query = {
  'key': API_KEY,
  'token': AUTH_TOKEN
  }

  response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
  ) 

  JSON_response = json.loads(response.text)

  seen = []
  duplicates = []
  for obj in JSON_response:
      job_no = obj["name"].split('-')[0].replace("#", " ")
      if not (any(c.isalpha() for c in job_no)):
          if job_no.strip() not in seen:
              seen.append(job_no.strip())
          else: duplicates.append(job_no.strip())

  if(len(duplicates) > 0):
    body = "<b size=40px> Duplicate Cards: </b>"

    for duplicate in duplicates:
       body = body + "<li>" + duplicate + "</li>"
    print("Duplicates in: " + name + "Board, sending email")
    emailer.send_email(EMAIL_RECEIVER, "Duplicates Found in Board:" + name, body)
  else:
     print("No duplicates found in the provided board!")




def run_task():
  look_for_duplicates(FIT_OUT_BOARD, "Fit Out")
  look_for_duplicates(DRAFTING_BOARD, "Drafting")
  gc.collect()

if __name__ == "__main__":
    
    schedule.every(120).minutes.do(run_task)

    while True:
       schedule.run_pending()
       time.sleep(1)

