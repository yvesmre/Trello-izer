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
            list.append(attachment['url'].split('/c/')[1])

        return list
    except:
        return response.text

def gather_card_attachments(card):
    attachments = gather_attachments(card)

    child_cards = []

    for attachment in attachments:
        child_cards.append(import_card(attachment))

    return child_cards





f = open(os.getcwd() + '/' + '668f75c9a0a530c3832a2cc9.json', mode='w' )

card_checklist = {}

for cards in gather_card_attachments('668f75c9a0a530c3832a2cc9'):
    checklist = import_checklist(cards['id'])
    for checkbox in checklist:
        json.dump(checkbox['checkItems']['state'], indent=4, fp=f)


f.close()