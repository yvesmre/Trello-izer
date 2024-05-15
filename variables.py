import os
from dotenv import load_dotenv
import configparser

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_KEY = os.getenv("API_KEY")
FIT_OUT_BOARD = os.getenv("FIT_OUT_BOARD")
DRAFTING_BOARD = os.getenv("DRAFTING_BOARD")
BUILD_CHECKLIST_TEMPLATE = os.getenv("BUILD_CHECKLIST")

FIT_OUT_BUILD_TEMPLATE = os.getenv("FIT_OUT_BUILD_TEMPLATE")


TEST_LIST = os.getenv("TEST_LIST")
TEST_BOARD = os.getenv("TEST_BOARD")




EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_CREDENTIALS = os.getenv("EMAIL_CREDENTIALS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# MYOB_ACCESS_CODE = os.getenv("MYOB_ACCESS_CODE")
MYOB_API_KEY = os.getenv("MYOB_API_KEY")
MYOB_API_SECRET = os.getenv("MYOB_API_SECRET")


config = configparser.ConfigParser()

if not os.path.isfile('config.ini'):

    config["SETTINGS"] = {"write to excel":  False, "different excel destination": True}
    config["SECRETS"] = {
                        'myob api key': '', 
                        'myob api secret': '',
                        "trello auth token": '',
                        'trello api key':''
                        }
    config['BOARD and LIST IDS'] = {"fit out board": '', "drafting board": ""}
    config["FILE LOCATIONS"] = {"excel schedule read": '', "excel schedule write": ''}

    configfile = open('config.ini', 'w')
    with configfile:
        config.write(configfile)
    configfile.close()


config.read('config.ini')
    
WRITE_TO_EXCEL = config["SETTINGS"].getboolean("write to excel")
DIFFERENT_DESTINATION_EXCEL = config["SETTINGS"].getboolean("different excel destination")
EXCEL_SPREADSHEET_READ = config["FILE LOCATIONS"]["excel schedule read"]
EXCEL_SPREADSHEET_WRITE = config["FILE LOCATIONS"]["excel schedule write"]