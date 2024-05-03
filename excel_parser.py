import openpyxl

def parse_spreadsheet_for_pickslips_and_due_dates(file):
    data = {}

    dataframe = openpyxl.load_workbook(file)
    spreadsheet = dataframe.active

    for col in spreadsheet.iter_cols(1, spreadsheet.max_column):
        column = []
        if col[0].value == "Pickslip" or col[0].value == "Creation date":
            for row in range(1, spreadsheet.max_row):
                    column.append(col[row].value)
            data[col[0].value] = column


    return data


print(parse_spreadsheet_for_pickslips_and_due_dates("Test Excel Sheet.xlsx"))