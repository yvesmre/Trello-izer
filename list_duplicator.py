from import_myob_data import *
from trello_imports import *
from trello_exports import *
import tkinter

def copy_paste(master_job, child_job):

    import_myob()


    board = []

    if not USE_TESTING_LIST:
        for s in BOARDS_TO_SEARCH:
            board.extend(import_cards_with_custom_fields_from_board(s))
    else:
        board = import_cards_with_custom_fields_from_board(TEST_BOARD)


    master_card = None
    child_card = None

    json_out = None
    card_data = None
    for card in board:

        card_id = card['id']
        job_no = card["name"].split('-')[0].replace('#','').strip()
        if(not job_no.isnumeric() or "DRAFTING" in card['name']): 
            continue
        
        if(job_no == master_job):
            master_card = card
        if(job_no == child_job):
            child_card = card
        
    
        if(master_card and child_card): break

    master_checklist = sorted(import_checklist(master_card['id']), key=lambda k: k.get('pos', 0))

    for checklist in import_checklist(child_card['id']):
        delete_list(child_card['id'], checklist['id'])    

    for checklist in master_checklist:
        new_list = (create_list(child_card['id'], checklist['name'], None))

        for checkitem in checklist['checkItems']:
            create_list_item(new_list['id'], checkitem['name'], True if not checkitem['state'] == "incomplete" else False, checkitem['pos'])

    return json_out, card_data


if __name__ == "__main__":

    editing = False
    
    def all_children (wid) :
        _list = wid.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list
    

    def force_list():
        copy_paste(e1.get(), e2.get())
        return

    def run():
        thread = Thread(target=force_list)
        thread.start()

    m = tkinter.Tk(className=" List Duplicator")
    
    m.minsize(512, 512)
    m.columnconfigure(1, weight=1)
    m.columnconfigure(3, weight=1)

    m.rowconfigure(index=list(range(0, 3)), weight=1)

    tkinter.Label(m, text='Job No.').grid(row=0, column=1)

    e1 = tkinter.Entry(m)
    e1.grid(row=1, column=0)

    e2 = tkinter.Entry(m)
    e2.grid(row=1, column=2)

    start_button = tkinter.Button(m, text="Copy Checklists", command=run)
    start_button.grid(row=2, column=1)


    m.mainloop()