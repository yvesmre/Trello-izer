from excel_parser import *
from variables import *
from trello_exports import *
from trello_imports import *
from datetime import date
from import_myob_data import *
import shutil
import tkinter
from openpyxl.styles import Font
import tkinter
from functools import partial
from trello_imports import *
import os, subprocess, platform
from openpyxl import load_workbook
from openpyxl.styles import Font
import shutil
from pandas import ExcelWriter
from openpyxl.cell import MergedCell
from variables import *

def all_children (wid) :
    _list = wid.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list

def fit_text_to_widget(text_widget):
    # Get the number of lines and the longest line's length
    num_lines = int(text_widget.index('end-1c').split('.')[0])
    longest_line_length = max(len(line) for line in text_widget.get("1.0", "end-1c").split('\n'))

    # Calculate the widget's required height and width
    height = int(int(longest_line_length/(512/8))*2)
    width = int(min(longest_line_length, 512/8))

    # Resize the widget to fit the text
    text_widget.config(width=width, height=height)


def look_for_cards_to_delete(screen):
    
    board = []

    if not USE_TESTING_LIST:
        for s in BOARDS_TO_SEARCH:
            board.extend(import_cards_with_custom_fields_from_board(s))
    
    else: board = import_cards_with_custom_fields_from_board(TEST_BOARD)

    def threadify_delete_card(event):
        print(event.widget.get("1.0",'end-1c'))
        # thread = Thread(target=deploy_card, args=(event, ))
        # thread.start()


    for i in range(len(board)):
        card = board[i]
        name = card['name']
        if '-' in name and "DRAFTING" not in name:
            display = tkinter.Text(screen)
            display.insert('1.0', name)
            fit_text_to_widget(display)
            display.grid(row=2+i, column=1)
            display.bind("<Button-1>", threadify_delete_card)
            

    
    return
        
if __name__ == "__main__":
    # warnings.simplefilter(action='ignore', category=FutureWarning)

    def look_for_cards():
        thread = Thread(target = look_for_cards_to_delete, args=(m,))

        thread.start()



    
    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)
    m.rowconfigure(1, weight=1)

    m.rowconfigure(list(range(2,50)), weight=1)

    start_button = tkinter.Button(m, text="Look for Cards to be Deleted", command=look_for_cards, width=24, height=4)
    start_button.grid(row=1, column=1)

    m.mainloop()

