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

            if len(myob_discrepancies) > 0:
                json_out[job_no] = {"myob": myob_lines, 'trello': trello_lines, 'myob discrepancies': myob_discrepancies, 'trello discrepancies': trello_discrepancies}

            break

    return json_out


if __name__ == "__main__":

    def hello():
        entry = e1.get()
        if(entry.isnumeric()):
            
            discrepancy = look_for_discrepancy(entry)
    
            if(discrepancy):
                myob_header = tkinter.Label(m, text="Myob Discrepancies")
                # myob_header.config(bg='black')
                myob_header.grid(row=2, column=1)

                ms_myob = tkinter.Label(m, text=discrepancy[entry]['myob discrepancies'])
                ms_myob.config(bg='darkgray')
                ms_myob.grid(row=3, column=1)


                trello_header = tkinter.Label(m, text="Trello Discrepancies")
                # trello_header.config(bg='black')
                trello_header.grid(row=2, column=3)

                ms_trello = tkinter.Label(m, text=discrepancy[entry]['trello discrepancies'])
                ms_trello.config(bg='gray')
                ms_trello.grid(row=3, column=3)
            

    m = tkinter.Tk()
    
    m.minsize(512, 512)
    tkinter.Label(m, text='Job No.').grid(row=0)

    e1 = tkinter.Entry(m)
    e1.grid(row=0, column=1)

    start_button = tkinter.Button(m, text="Look for Discrepancies", command=hello)
    start_button.grid(row=1, column=1)

    m.mainloop()