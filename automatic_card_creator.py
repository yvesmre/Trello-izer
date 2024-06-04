from excel_parser import *
from variables import *
from trello_exports import *
from trello_imports import *
from datetime import date
from import_myob_data import *
import shutil


# Main python class and function where everything happens
def main():

    import_myob()

    updates = {}
    orders = parse_spreadsheets_for_orders(EXCEL_SPREADSHEET_READ)

    if(len(orders) == 0):
        print("No cards to be created!")
        return
    
    cards_created = len(orders)
    print(str(cards_created) + " possible cards found!")

    for order in orders:
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
            for checklist in checklists:
                delete_list(fit_out_card_id, checklist['id'])
            fit_out_description = "Dealer: "+ order.headers[1].split('-')[0] + "\nContact: " + order.headers[1].split('-')[1] + '\n'

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

    update_row(EXCEL_SPREADSHEET_WRITE if DIFFERENT_DESTINATION_EXCEL else EXCEL_SPREADSHEET_READ, updates)
    
if __name__ == "__main__":
    main()


