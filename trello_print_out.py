import tkinter
from functools import partial
from trello_imports import *
from docx import Document
from docx.shared import Inches
import os

def fit_text_to_widget(text_widget):
    # Get the number of lines and the longest line's length
    num_lines = int(text_widget.index('end-1c').split('.')[0])
    longest_line_length = max(len(line) for line in text_widget.get("1.0", "end-1c").split('\n'))

    # Calculate the widget's required height and width
    height = int(int(longest_line_length/(512/8))*2)
    width = int(min(longest_line_length, 512/8))

    # Resize the widget to fit the text
    text_widget.config(width=width, height=height)

def all_children (wid) :
    _list = wid.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list




def create_spreadsheet(board_id, job_no, filename):

    #Hacky way of going about this, tbh
    if not os.path.exists(os.getcwd() + "/" + filename.split('/')[1]) :
        os.makedirs(os.getcwd() + "/" + filename.split('/')[1])

    board = import_cards_with_custom_fields_from_board(board_id)

    to_json = {"Checklist": [], 
                'Part No.': [], 
            #    "Member": [], "Completion": [], 
            #    "Card Last Modified": []
                    }

    user_to_name = {}
    for card in board:
        checklists = import_checklist(card['id'])

        card_name = card['name']
        if not (card_name.split('-')[0].replace('#', '').strip() == job_no): continue

        for obj in checklists:

            part_found = None
            for checklist_item in obj["checkItems"]:
                if("Part No." in checklist_item['name']):
                    part_found = checklist_item['name']
                    break
            
    
            to_json['Checklist'].append(obj['name'])
            to_json['Part No.'].append('N/A' if not part_found else part_found)

        break

    frame = pd.DataFrame(data=to_json)


    writer = StyleFrame.ExcelWriter(os.getcwd() + filename)
    sf = StyleFrame(frame)

    #   sf.set_column_width(columns='Card Title', width=25)
    sf.set_column_width(columns='Checklist', width=70)
    sf.set_column_width(columns='Part No.', width=50)
    #   sf.set_column_width(columns='Member', width=25)
    #   sf.set_column_width(columns='Card Last Modified', width=20)
    #   sf.set_column_width(columns='Completion', width=20)
    sf.to_excel(excel_writer=writer, row_to_add_filters=0,index=False)


    writer.close()




if __name__ == "__main__":
    def search_card(widget):
        board = import_cards_with_custom_fields_from_board(FIT_OUT_BOARD if not USE_TESTING_LIST else TEST_LIST)

        create_spreadsheet(board_id=FIT_OUT_BOARD, job_no=widget.get(), filename="/output/" + widget.get() + ".xlsx")
        for child in all_children(m):
            if type(child) == tkinter.Text:
                child.destroy()

        for card in board:
            card_id = card['id']
            job_no = card["name"].split('-')[0].replace('#','').strip()

            if (job_no==widget.get()):
                
                checklists = import_checklist(card_id)

                name = tkinter.Text(m)
                name.insert("1.0", card["name"])
                name.grid(row=3, column=1)
                fit_text_to_widget(name)

                for obj in checklists:
                    text = tkinter.Text(m, wrap="word")
                    text.insert('1.0', obj['name'].strip())
                    text.grid(row=4+checklists.index(obj), column=1)
                    fit_text_to_widget(text)
                 



    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)

    tkinter.Label(m, text='Job No.').grid(row=0, column=1)

    e1 = tkinter.Entry(m)
    e1.grid(row=1, column=1)

    start_button = tkinter.Button(m, text="Get Card Details", command=partial(search_card, e1))
    start_button.grid(row=2, column=1)

    m.mainloop()

