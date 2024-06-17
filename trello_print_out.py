import tkinter
from functools import partial
from trello_imports import *

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

if __name__ == "__main__":
    def search_card(widget):
        board = import_cards_with_custom_fields_from_board(FIT_OUT_BOARD if not USE_TESTING_LIST else TEST_LIST)



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
