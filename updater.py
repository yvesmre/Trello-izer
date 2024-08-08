from trello_imports import *
from trello_exports import *
import requests
import json
import tkinter
from functools import partial


def retrieve_child_completion(card):

    card_checklist = {}

    total = 0
    complete = 0

    for cards in gather_card_attachments(card):
        checklist = import_checklist(cards['id'])
        # if('DRAFTING' in cards['name']): continue
        for checkbox in checklist:
            for check_item in checkbox['checkItems']:
                total = total + 1

                if check_item['state'] == 'complete':
                    complete = complete + 1


    return total, complete


def update_parent_cards():


    search_indicator = tkinter.Label(m, text="Updating...")
    search_indicator.config(bg="green")
    search_indicator.grid(row=4,column=1)

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

    search_indicator.destroy()



if __name__ == "__main__":
    def search_card():
        thread = Thread(target=update_parent_cards)
        thread.start()
                 
    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)

    start_button = tkinter.Button(m, text="Update cards", command=search_card, width=30, height=6)
    start_button.grid(row=1, column=1)

    m.mainloop()

