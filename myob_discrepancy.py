from collections import OrderedDict
from import_myob_data import *
from trello_imports import *
import tkinter

def look_for_discrepancy(job):

    import_myob()

    board = import_cards_with_custom_fields_from_board(FIT_OUT_BOARD)
    
    json_out = None

    for card in board:
        card_id = card['id']
        job_no = card["name"].split('-')[0].replace('#','').strip()
        if(not job_no.isnumeric()): 
            continue
        
        if(job_no == job):
            json_out = {}
            checklists = import_checklist(card_id)
            myob_data =  search_myob(job_no)["Lines"] if search_myob(job_no) else None
            myob_lines = []
            trello_lines = []
            if myob_data:
                for line in myob_data: 
                    if(not line["Type"] == "Header"): 
                        myob_lines.append(' '.join(line["Description"].split()))

            for obj in checklists:
                trello_lines.append(obj['name'].strip())


            myob_discrepancies = []
            trello_discrepancies = []
            for items in myob_lines:
                if(items not in trello_lines):
                    myob_discrepancies.append(items)
                
            for items in trello_lines:
                if(items not in myob_lines):
                    trello_discrepancies.append(items)

            if len(myob_discrepancies) > 0 or len(trello_discrepancies) > 0:
                json_out[job_no] = {"myob": myob_lines, 'trello': trello_lines, 'myob discrepancies': myob_discrepancies, 'trello discrepancies': trello_discrepancies}

            break

    # print(json.dumps(json_out, indent=4))

    return json_out


if __name__ == "__main__":

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
        height = int(num_lines*2)
        width = longest_line_length

        # Resize the widget to fit the text
        text_widget.config(width=width, height=height)

    def run_discrepancy_lookup():
        children = all_children(m)

        for child in children:
            if type(child) == tkinter.Text:
                child.destroy()

        entry = e1.get()
        if(entry.isnumeric()):
            
            discrepancy = look_for_discrepancy(entry)
    
            if(discrepancy):
                myob_header = tkinter.Label(m, text="Myob Discrepancies")
                # myob_header.config(bg='black')
                myob_header.grid(row=2, column=1)

                for i in range(len(discrepancy[entry]['myob discrepancies'])):
                    myob_disc = discrepancy[entry]['myob discrepancies'][i]
                    ms_myob = tkinter.Text(m, wrap="word")
                    ms_myob.insert('1.0', myob_disc)
                    ms_myob.config(bg='darkgray' if not i % 2 == 0 else 'gray')
                    ms_myob.grid(row=i+3, column=1)
                    ms_myob.config(state="disabled")
                    fit_text_to_widget(ms_myob)
                   
                trello_header = tkinter.Label(m, text="Trello Discrepancies")
                # trello_header.config(bg='black')
                trello_header.grid(row=2, column=3)

                for i in range(len(discrepancy[entry]['trello discrepancies'])):
                    trello_disc =discrepancy[entry]['trello discrepancies'][i]
                    ms_trello = tkinter.Text(m, wrap="word")
                    ms_trello.insert('1.0', trello_disc)
                    ms_trello.config(bg='gray' if i % 2 == 0 else 'lightgray')
                    ms_trello.grid(row=i+3, column=3)
                    ms_trello.config(state="disabled")
                    fit_text_to_widget(ms_trello)
                   
                
            

    m = tkinter.Tk()
    
    m.minsize(512, 512)
    m.columnconfigure(1, weight=1)
    m.columnconfigure(3, weight=1)

    tkinter.Label(m, text='Job No.').grid(row=0)

    e1 = tkinter.Entry(m)
    e1.grid(row=0, column=1)

    start_button = tkinter.Button(m, text="Look for Discrepancies", command=run_discrepancy_lookup)
    start_button.grid(row=1, column=1)

    m.mainloop()