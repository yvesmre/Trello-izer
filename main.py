from excel_parser import *
from variables import *
from create_card import *
from datetime import date

def main():

    updates = {}
    orders = parse_spreadsheets_for_orders("K-Drive Schedule.xlsx")

    if(len(orders) == 0):
        print("No cards to be created!")
        return
    
    for order in orders:
        create_card(TEST_LIST, str(order.job_number) + "-" + order.client, "", FIT_OUT_BUILD_TEMPLATE)
        updates[str(order.job_number)] = date.today()


    update_row("K-Drive Schedule.xlsx", updates)

if __name__ == "__main__":
    main()


