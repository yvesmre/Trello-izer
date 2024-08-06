from trello_imports import *
from trello_exports import *
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
    # f = open(os.getcwd() + '/' + card + '.json', mode='w' )

    card_checklist = {}

    total = 0
    complete = 0

    for cards in gather_card_attachments(card):
        checklist = import_checklist(cards['id'])
        # if('DRAFTING' in cards['name']): continue
        for checkbox in checklist:
            for check_item in checkbox['checkItems']:
                total = total + 1
                # json.dump(check_item, indent=4, fp=f)
                if check_item['state'] == 'complete':
                    complete = complete + 1
    # f.close()

    return total, complete


def update_parent_cards():
    board = import_cards_with_custom_fields_from_board(TEST_BOARD)

    cards = []
    for card in board:

        card_name = card['name']
        desc = card['desc']
        if not (card_name.split('-')[0].replace('#', '').strip().isnumeric()): continue
        
        total, complete = retrieve_child_completion(card['id'])


        desc = get_desc(card['id'])

        if 'Completed: ' in desc:
            desc = desc.split("\n\n ## `Completed:")[0]

        update_card(card['id'], desc + "\n\n ## `Completed: " + str(complete/total * 100) + "%`")


update_parent_cards()