from excel_parser import *
from variables import *
from trello_exports import *
from trello_imports import *
from datetime import date
from import_myob_data import *
import shutil
import tkinter

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

def deploy_card(event):
    make_card(event.widget.get("1.0",'end-1c').split('-')[0])
    cards_to_be_made(event.widget.master)


def cards_to_be_made(screen):


    search_indicator = tkinter.Label(m, text="Searching...")
    search_indicator.config(bg="green")
    search_indicator.grid(row=2,column=1)


    def threadify_deploy_card(event):
        thread = Thread(target=deploy_card, args=(event, ))
        thread.start()

    import_myob()

    orders = parse_spreadsheets_for_orders(EXCEL_SPREADSHEET_READ)

    for child in all_children(screen):
        if(type(child) == tkinter.Text):
            child.destroy()

    for i in range(len(orders)):
        order = orders[i]

        myob = search_myob(order.job_number)
        if not myob:
            continue

        display = tkinter.Text(screen)
        display.insert('1.0', str(order.job_number) + "-" + order.client)
        fit_text_to_widget(display)
        display.grid(row=2+i, column=1)
        display.bind("<Button-1>", threadify_deploy_card)

    print("Done looking for cards")
    search_indicator.destroy()


def make_card(job_no):

    import_myob()

    updates = {}
    orders = parse_spreadsheets_for_orders(EXCEL_SPREADSHEET_READ)

    if(len(orders) == 0):
        print("No cards to be created!")
        return
    
    order = None
    for ord in orders:
        if(str(ord.job_number) == job_no):
            order = ord
            break

    myob = search_myob(order.job_number)
    if myob:
        lines = search_myob(order.job_number)["Lines"]
        order.set_lines(lines)
    else: print(str(order.job_number) + " Does not have a MYOB entry! Skipping")
    
    if(len(order.lines) > 0): # Only do job cards for ones with MYOB entries ### Could be a setting later

        fit_out_card = create_card(FIT_OUT_TODO_LIST if not USE_TESTING_LIST else TEST_LIST, str(order.job_number) + " - " + order.client, "", FIT_OUT_BUILD_TEMPLATE)
        fit_out_card_id = fit_out_card["id"]
        fit_out_card_url = fit_out_card["url"]
        
        checklists = import_checklist(fit_out_card_id)
        
        # Template Cards may come with Template Lists, disregard and delete. 
        # for checklist in checklists:
        #     delete_list(fit_out_card_id, checklist['id'])
        
        try:
            fit_out_description = "Dealer: "+ order.headers[1].split('-')[0] + "\nContact: " + order.headers[1].split('-')[1] + '\n'
        except:
            fit_out_description = ""

        if len(order.headers) > 2:
            for i in range(2, len(order.headers)):
                fit_out_description = fit_out_description + "\n##" + "**" + order.headers[i] + "**"
        update_card(fit_out_card_id, fit_out_description)
        drafting_card = create_card(DRAFTING_TODO_LIST if not USE_TESTING_LIST else TEST_LIST, str(order.job_number) + " - DRAFTING - " + order.client, "", DRAFTING_CARD_TEMPLATE)

        create_attachment(drafting_card["id"], fit_out_card_url)
        create_attachment(fit_out_card_id, drafting_card["url"])

        for line in order.lines:
            create_list(fit_out_card_id, line, BUILD_CHECKLIST_TEMPLATE)

        updates[str(order.job_number)] = date.today()

    if DIFFERENT_DESTINATION_EXCEL:
        shutil.copyfile(EXCEL_SPREADSHEET_READ, EXCEL_SPREADSHEET_WRITE)

    update_row(EXCEL_SPREADSHEET_WRITE if DIFFERENT_DESTINATION_EXCEL else EXCEL_SPREADSHEET_READ, updates) if WRITE_TO_EXCEL else None

    print("Run Done, made ", len(updates), " cards")
        
        
if __name__ == "__main__":

    def look_for_cards():
        thread = Thread(target = cards_to_be_made, args=(m,))
        thread.start()
    
    m = tkinter.Tk()
    m.config(bg="black")
    
    m.minsize(384, 384)
    m.columnconfigure(1, weight=1)
    m.rowconfigure(1, weight=1)

    m.rowconfigure(list(range(2,50)), weight=1)

    start_button = tkinter.Button(m, text="Look for Cards to be Made", command=look_for_cards, width=24, height=4)
    start_button.grid(row=1, column=1)

    m.mainloop()

