from excel_parser import *
from variables import *
from create_card import *
from datetime import date
from import_myob_data import *
def main():

    # import_myob()


    updates = {}
    orders = parse_spreadsheets_for_orders("K-Drive Schedule.xlsx")

    if(len(orders) == 0):
        print("No cards to be created!")
        return
    
    for order in orders:
        myob = search_myob(order.job_number)
        if myob:
            lines = search_myob(order.job_number)["Lines"]
            order.set_lines(lines)
            print(str(order))
        else: print(str(order.job_number) + " Does not have a MYOB entry! Skipping")
        # create_card(TEST_LIST, str(order.job_number) + "-" + order.client, "", FIT_OUT_BUILD_TEMPLATE)
        # updates[str(order.job_number)] = date.today()


    # update_row("K-Drive Schedule.xlsx", updates)

if __name__ == "__main__":
    main()


