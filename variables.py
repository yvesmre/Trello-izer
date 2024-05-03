import os
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_KEY = os.getenv("API_KEY")
PRODUCTION_BOARD = os.getenv("PRODUCTION_BOARD")