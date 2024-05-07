import openpyxl
import pandas as pd
import math
import datetime

keywords = ["Job No.", "Customer", "Client", "Quote Status", "Purchase Order Date", "Trello Card Created"]

class Order():
    def __init__(self, job_number, customer, client):
        self.job_number = job_number
        self.customer = customer
        self.client = client
    
    def __str__(self):
        return f"{self.job_number} {self.customer} {self.client}"

def parse_spreadsheet_for_pickslips_and_due_dates(file):
    data = []

    spreadsheet  = pd.read_excel(file, keep_default_na=False)

    spreadsheet.columns = spreadsheet.iloc[32]

    for index, row in spreadsheet.loc[:, keywords].iterrows():
        if(row['Quote Status'] == "Won" and type(row["Purchase Order Date"]) is not float and type(row['Trello Card Created']) is not datetime.datetime and type(row['Customer']) is str):
            if(row['Trello Card Created'].lower() != "n/a" and row['Trello Card Created'].lower() != "new"):
                if (type(row['Purchase Order Date']) is datetime.datetime and row['Purchase Order Date'].year >= 2024):
                # if (type(row['Purchase Order Date']) is datetime.datetime and row['Purchase Order Date'].year >= 2024) or type(row['Purchase Order Date']) is str:
                    data.append(Order(row['Job No.'], row['Customer'], row['Client']))

    return data


def update_row(file, updates):
    spreadsheet = openpyxl.load_workbook(file)

    sh = spreadsheet.active 
  
    for row in sh.iter_rows(): 
        if str(row[0].value) in updates:
            row[18].value = updates.pop(str(row[0].value))

    spreadsheet.save("test output.xlsx")
        

    