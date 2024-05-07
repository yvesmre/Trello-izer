from excel_parser import *
from variables import *
from create_card import *
from datetime import date

def main():

    updates = {}
    orders = parse_spreadsheet_for_pickslips_and_due_dates("test output.xlsx")

    if(len(orders) == 0):
        print("No cards to be created!")
        return

    for order in orders:
        create_card(TEST_LIST, str(order.job_number) + "-" + order.client, "", "")
        updates[str(order.job_number)] = date.today()


    update_row("test output.xlsx", updates)

if __name__ == "__main__":
    main()


