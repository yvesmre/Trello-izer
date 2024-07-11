from trello_imports import *
import requests
import json


query = {
'key': API_KEY,
'token': AUTH_TOKEN
}

def gather_attachments(card):

    url = "https://api.trello.com/1/cards/" + card + "/attachments"

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query
    )

    try: 
        JSON = json.loads(response.text)
        list = []

        for attachment in JSON:
            list.append(attachment['url'])

        return list
    except:
        return response.text





print(gather_attachments('668f3f9f55e1d1dc64077cd4'))