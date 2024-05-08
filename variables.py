import os
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_KEY = os.getenv("API_KEY")
FIT_OUT_BOARD = os.getenv("FIT_OUT_BOARD")
DRAFTING_BOARD = os.getenv("DRAFTING_BOARD")
BUILD_CHECKLIST_TEMPLATE = os.getenv("BUILD_CHECKLIST")


TEST_LIST = os.getenv("TEST_LIST")
TEST_BOARD = os.getenv("TEST_BOARD")

TEST_FILENAME = os.getenv("TEST_FILENAME")


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_CREDENTIALS = os.getenv("EMAIL_CREDENTIALS")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")