from collections import OrderedDict
from import_myob_data import *
from trello_imports import *
from trello_exports import *
import tkinter

def look_for_discrepancy(job):

    import_myob()


    board = []

    for s in BOARDS_TO_SEARCH:
        board.extend(import_cards_with_custom_fields_from_board(s))
        

    json_out = None
    card_data = None
    for card in board:
        card_id = card['id']
        job_no = card["name"].split('-')[0].replace('#','').strip()
        if(not job_no.isnumeric()): 
            continue
        
        if(job_no == job):
            card_data=card
            json_out = {}
            # checklists = import_checklist(card_id)

            
            myob_data =  search_myob(job_no)["Lines"] if search_myob(job_no) else None
            myob_lines = []
            trello_lines = []

            trello_table = {}
            if myob_data:
                for line in myob_data: 
                    if(not line["Type"] == "Header"): 
                        myob_lines.append(' '.join(line["Description"].split()))

            # for obj in checklists:
            #     trello_lines.append(obj['name'].strip())
            #     trello_table[obj['name'].strip()] = obj['id']


            myob_discrepancies = []
            trello_discrepancies = []
            for items in myob_lines:
                if(items not in trello_lines):
                    myob_discrepancies.append(items)
                
            for items in trello_lines:
                if(items not in myob_lines):
                    trello_discrepancies.append(items)

            if len(myob_discrepancies) > 0 or len(trello_discrepancies) > 0:
                json_out[job_no] = {"myob": myob_lines, 'trello': trello_lines, 'myob discrepancies': myob_discrepancies, 'trello discrepancies': trello_discrepancies, 'trello table': trello_table}

            break


    return json_out, card_data


if __name__ == "__main__":

    editing = False
    
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
        height = int(int(longest_line_length/(512/8))*2.5)
        width = int(min(longest_line_length, 512/8))

        # Resize the widget to fit the text
        text_widget.config(width=width, height=height)


    def run_discrepancy_lookup():
        children = all_children(m)

        for child in children:
            if type(child) == tkinter.Text:
                child.destroy()
            if(type(child) ==tkinter.Label):
                if(not child['text'] == "Job No." and not child['text'] == "Toggle Editing" ):
                    child.destroy()


        label = tkinter.Label(m, text="Searching...")
        label.grid(row=4, column=1)
        label.config(bg="green")

        entry = e1.get()
        if(entry.isnumeric()):
            
            discrepancy, card_data = look_for_discrepancy(entry)
    
            def remove_list(event):
                delete_list(card_data['id'], discrepancy[entry]['trello table'][event.widget.get("1.0",'end-1c')])
                # run_discrepancy_lookup()

            def build_list(event):
                create_list(card_data['id'], event.widget.get("1.0",'end-1c'), BUILD_CHECKLIST_TEMPLATE)
                # run_discrepancy_lookup()

            def callback(event):
                global editing
                if not editing: return
                thread = Thread(target=build_list, args=(event,))
                thread.start()

            def callback2(event):
                global editing
                if not editing: return
                thread = Thread(target=remove_list, args=(event,))
                thread.start()    


            if(discrepancy):
                myob_header = tkinter.Label(m, text="Myob Discrepancies")
                # myob_header.config(bg='black')
                myob_header.grid(row=2, column=1)

                for i in range(len(discrepancy[entry]['myob discrepancies'])):
                    myob_disc = discrepancy[entry]['myob discrepancies'][i]
                    ms_myob = tkinter.Text(m, wrap="word")
                    ms_myob.insert('1.0', myob_disc)
                    ms_myob.config(bg='gray30', fg="white")
                    ms_myob.grid(row=i+3, column=1)
                    ms_myob.config(state="disabled")
                    ms_myob.bind('<Button-1>', callback)
                    fit_text_to_widget(ms_myob)
                   
                trello_header = tkinter.Label(m, text="Trello Discrepancies")
                # trello_header.config(bg='black')
                trello_header.grid(row=2, column=3)

                for i in range(len(discrepancy[entry]['trello discrepancies'])):
                    trello_disc =discrepancy[entry]['trello discrepancies'][i]
                    ms_trello = tkinter.Text(m, wrap="word")
                    ms_trello.insert('1.0', trello_disc)
                    ms_trello.config(bg='gray30', fg="white")
                    ms_trello.grid(row=i+3, column=3)
                    ms_trello.config(state="disabled")
                    ms_trello.bind('<Button-1>', callback2)
                    fit_text_to_widget(ms_trello)
            
            label.destroy()
            if not discrepancy:
                label = tkinter.Label(m, text="No Differences Found!")
                label.grid(row=4, column=1)
                label.config(bg="red")


    

    def run():
        thread = Thread(target=run_discrepancy_lookup)
        thread.start()

    def toggle_edit(event):
        global editing
        editing = not editing
        edit_toggle.config(bg='green' if editing else 'red')

    m = tkinter.Tk(className=" MYOB Trello Comparator")
    
    m.minsize(512, 512)
    m.columnconfigure(1, weight=1)
    m.columnconfigure(3, weight=1)

    m.rowconfigure(index=list(range(3, 50)), weight=1)

    tkinter.Label(m, text='Job No.').grid(row=0)

    e1 = tkinter.Entry(m)
    e1.grid(row=0, column=1)

    start_button = tkinter.Button(m, text="Look for Discrepancies", command=run)
    start_button.grid(row=1, column=1)


    edit_toggle = tkinter.Label(m, text="Toggle Editing")
    edit_toggle.grid(row=0, column=2)
    edit_toggle.config(bg='green' if editing else 'red')
    edit_toggle.bind('<Button-1>', toggle_edit)

    m.mainloop()