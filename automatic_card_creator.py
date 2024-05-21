from excel_parser import *
from variables import *
from trello_exports import *
from datetime import date
from import_myob_data import *
import shutil


# Main python class and function where everything happens
def main():

    import_myob()

    LIST_DESINATION = TEST_LIST # if USE_TEST_LIST else FIT_OUT_BOARD

    # print("Hello")
    updates = {}
    orders = parse_spreadsheets_for_orders(EXCEL_SPREADSHEET_READ)

    if(len(orders) == 0):
        print("No cards to be created!")
        return
    
    for order in orders:
        myob = search_myob(order.job_number)
        if myob:
            lines = search_myob(order.job_number)["Lines"]
            order.set_lines(lines)
        else: print(str(order.job_number) + " Does not have a MYOB entry! Skipping")
        
        if(len(order.lines) > 0): # Only do job cards for ones with MYOB entries ### Could be a setting later
            card = create_card(TEST_LIST, str(order.job_number) + "-" + order.client, "", FIT_OUT_BUILD_TEMPLATE)["id"]
            create_card(TEST_LIST, str(order.job_number) + "- DRAFTING -" + order.client, "", DRAFTING_CARD_TEMPLATE)["id"]
            for line in order.lines:
                create_list(card, line, BUILD_CHECKLIST_TEMPLATE)
            updates[str(order.job_number)] = date.today()

    if DIFFERENT_DESTINATION_EXCEL:
        shutil.copyfile(EXCEL_SPREADSHEET_READ, EXCEL_SPREADSHEET_WRITE)

    update_row(EXCEL_SPREADSHEET_WRITE if DIFFERENT_DESTINATION_EXCEL else EXCEL_SPREADSHEET_READ, updates)

if __name__ == "__main__":
    main()


