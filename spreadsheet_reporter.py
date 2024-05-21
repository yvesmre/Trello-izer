from variables import *
import trello_imports
import datetime

if __name__ == "__main__":
    trello_imports.create_excel_file(FIT_OUT_BOARD,  "/reports/" +  str(datetime.datetime.now()).replace(':','.') +  " fit out report.xlsx")
