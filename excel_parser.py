import openpyxl
import pandas as pd
import math
import datetime

keywords = ["Job No.", "Customer", "Client", "Quote Status", "Purchase Order Date", "Trello Card Created", "Invoice Date"]

class Order():
    def __init__(self, job_number, customer, client):
        self.job_number = job_number
        self.customer = customer
        self.client = client
        self.lines = []
        self.headers =[]
    
    def set_lines(self, lines):
        self.lines = []
        for line in lines:
            if(line["Type"] == "Header"): 
                self.headers.append(line["Description"])
            else:
                self.lines.append(line["Description"])

    def __str__(self):
        return f"{self.job_number} {self.customer} {self.client} {self.lines}"

def parse_spreadsheets_for_orders(file):
    data = []

    spreadsheet  = pd.read_excel(file, keep_default_na=False)

    column_index = None
    for index, row in spreadsheet.iterrows():
            if(row.iloc[0] == "Job No."):
               column_index = index

    spreadsheet.columns = spreadsheet.iloc[column_index]

    for index, row in spreadsheet.loc[:, keywords].iterrows():
        if (type(row["Job No."]) is int):
            if(row['Quote Status'] == "Won" and type(row['Trello Card Created']) is not datetime.datetime):
                if(row['Trello Card Created'].lower() != "n/a" and row['Trello Card Created'].lower() != "new"):
                        if(type(row["Invoice Date"]) is str):
                            order = Order(row['Job No.'], row['Customer'], row['Client'])
                            data.append(order)

    return data


def update_row(file, updates):
    spreadsheet = openpyxl.load_workbook(file)

    sh = spreadsheet.active 
  
    for row in sh.iter_rows(): 
        if str(row[0].value) in updates:
            row[18].value = updates.pop(str(row[0].value))

    spreadsheet.save(file)
        

    