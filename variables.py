import os
from dotenv import load_dotenv
import configparser

load_dotenv()

# BUILD_CHECKLIST_TEMPLATE = os.getenv("BUILD_CHECKLIST")

# FIT_OUT_BUILD_TEMPLATE = os.getenv("FIT_OUT_BUILD_TEMPLATE")

TEST_LIST = os.getenv("TEST_LIST")
TEST_BOARD = os.getenv("TEST_BOARD")

# EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# EMAIL_CREDENTIALS = os.getenv("EMAIL_CREDENTIALS")
# EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

config = configparser.ConfigParser()

if not os.path.isfile('config.ini'):

    config["SETTINGS"] = {"write to excel":  False, "different excel destination": True, "use testing board": False}
    config["SECRETS"] = {
                        'myob api key': '', 
                        'myob api secret': '',
                        "trello auth token": '',
                        'trello api key':''
                        }
    config['BOARD and LIST IDS'] = {"fit out board": '', "drafting board": "", 'fit out job card template': '', 'drafting card template':"", 'fit out job checklist template': ''}
    config["FILE LOCATIONS"] = {"excel schedule read": '', "excel schedule write": ''}
    config['DUPLICATE DETECTOR SETTINGS'] = {"sender address" : '', 'sender credentials': '', 'receiver address': ''}

    configfile = open('config.ini', 'w')
    with configfile:
        config.write(configfile)
    configfile.close()


config.read('config.ini')
    

AUTH_TOKEN = config["SECRETS"].get(option="trello auth token", fallback="")
API_KEY =  config["SECRETS"].get(option="trello api key", fallback="")

WRITE_TO_EXCEL = config["SETTINGS"].getboolean("write to excel")
DIFFERENT_DESTINATION_EXCEL = config["SETTINGS"].getboolean("different excel destination")
EXCEL_SPREADSHEET_READ = config["FILE LOCATIONS"].get(option="excel schedule read", fallback="Input.xlsx")
EXCEL_SPREADSHEET_WRITE = config["FILE LOCATIONS"].get(option="excel schedule write", fallback="Output.xlsx")

MYOB_API_KEY =  config["SECRETS"].get(option="myob api key", fallback="")
MYOB_API_SECRET = config["SECRETS"].get(option="myob api secret", fallback="")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_CREDENTIALS = os.getenv("EMAIL_CREDENTIALS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


FIT_OUT_BOARD = config['BOARD and LIST IDS'].get(option="fit out board", fallback="")
DRAFTING_BOARD = config['BOARD and LIST IDS'].get(option="drafting board", fallback="")

DRAFTING_CARD_TEMPLATE =  config['BOARD and LIST IDS'].get(option='drafting card template', fallback="")
FIT_OUT_BUILD_TEMPLATE = config['BOARD and LIST IDS'].get(option='fit out job card template', fallback="")
BUILD_CHECKLIST_TEMPLATE = config['BOARD and LIST IDS'].get(option='fit out job checklist template', fallback="")