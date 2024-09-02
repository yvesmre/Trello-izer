import requests
import json
import urllib.parse
import webbrowser
from variables import *
import listening_server
from threading import Thread
import pandas as pd


def acquire_code():
  url = "https://secure.myob.com/oauth2/account/authorize"
  data = {
    'client_id' :MYOB_API_KEY,
    'redirect_uri': 'http://localhost:8000/', 
    'response_type' :'code', 
    'scope':'CompanyFile'
  }

  response = requests.post(url, params=data)
  print(response.url)
  webbrowser.open(response.url)
 
def acquire_access(access_code):

  url = "https://secure.myob.com/oauth2/v1/authorize"

  headers = {
    # "Accept": "application/json",
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  data = {

    'code': (access_code), 
    'redirect_uri': 'http://localhost:8000/', 
    'client_id': MYOB_API_KEY,
    'client_secret': MYOB_API_SECRET,
    'scope': "CompanyFile", 
    'grant_type': 'authorization_code',
  }

  response = requests.post(url, headers=headers, data=data)

  text = response.text
  text = text.replace('\\', ' ')
  return text



def request_api(access_token):

  url = 'https://api.myob.com/accountright/'

  headers = {
    "Accept": "application/json",
    'Authorization': 'Bearer ' + access_token,
    'x-myobapi-cftoken': 'TWlndWVsLlJleWVzQGstZHJpdmUuY29tLmF1Okl0c21lZmVybmJyYWR5MSE=',
    'x-myobapi-key': MYOB_API_KEY,
    'x-myobapi-version': 'v2'
  }

  response = requests.request('GET', url, headers=headers)

  print(response.text) 

def request_sales(access_token):
  url = 'https://arl2.api.myob.com/accountright/4c1bf3cd-e1bf-4356-8bd1-1f0b053dc8f2/Sale/Order/Service/?$top=1000' 
  headers = {
    "Accept": "application/json",
    'Authorization': 'Bearer ' + access_token,
    'x-myobapi-key': MYOB_API_KEY,
    'x-myobapi-version': 'v2'
  }

  response = requests.request('GET', url, headers=headers)

  return json.dumps(json.loads(response.text.strip()))


def refresh_token(refresh_token):
  url = 'https://secure.myob.com/oauth2/v1/authorize'

  headers = {
    # "Accept": "application/json",
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  data = { 
    'client_id': MYOB_API_KEY,
    'client_secret': MYOB_API_SECRET,
    'refresh_token': refresh_token, 
    'grant_type': 'refresh_token',
  }

  response = requests.post(url, headers=headers, data=data)

  return response.text


def import_myob():
  if not os.path.isfile('access_token.json'):
    thread1 = Thread(target =  listening_server.run)
    thread1.start()
    acquire_code()
    thread1.join()

  JSON = json.load(open("access_token.json"))

  try:
    JSON = json.loads(refresh_token(JSON['refresh_token'])) 
  except:
      os.remove('access_token.json')
      import_myob()
      return   

  write_to_json("access_token.json", JSON)

  SALES_JSON = (request_sales(JSON['access_token']))

  if("Errors" in SALES_JSON):
    print("Invalid or expired access and refresh tokens, reacquiring and restarting")
    os.remove('access_token.json')
    import_myob()
    return

  dataframe = pd.read_json(SALES_JSON)
  dataframe.to_json('MYOB.json', indent=4)

def search_myob(job_no):
  file = open('MYOB.json')
  JSON = json.loads(json.dumps(json.load(file), indent=4))

  for key, val in JSON['Items'].items():
    for key, entries in val.items():
      if(key == "Number"):
        if(int(entries) == int(job_no)):
          file.close()
          return val

  file.close()
  return None


if __name__ == '__main__':
  import_myob()
    

def write_to_json(file, JSON):
  f = open(file, "w")
  with f as json_file:
    json.dump(JSON, json_file, indent=4)    
  f.close()