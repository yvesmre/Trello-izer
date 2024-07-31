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



def retrieve_child_completion(card):
    f = open(os.getcwd() + '/' + card + '/.json', mode='w' )

    card_checklist = {}

    total = 0
    complete = 0

    for cards in gather_card_attachments(card):
        checklist = import_checklist(cards['id'])
        for checkbox in checklist:
            for check_item in checkbox['checkItems']:
                total = total + 1
                json.dump(check_item, indent=4, fp=f)
                if check_item['state'] == 'complete':
                    complete = complete + 1
    f.close()

    return total, complete


print(json.dumps(get_desc('66a30ddd57ab65476ce164be'), indent=4))