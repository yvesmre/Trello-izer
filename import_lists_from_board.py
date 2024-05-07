# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
from variables import *

headers = {
  "Accept": "application/json"
}

query = {
  'key': API_KEY,
  'token': AUTH_TOKEN
}


def import_list(board):
    url = "https://api.trello.com/1/boards/" + board + "/lists"


    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

