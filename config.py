import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN","")
API_KEY = os.getenv("API_KEY","")
DB_NAME = "db/players.db"
HEADERS = {
    "Authorization" : API_KEY,
    "Content-Type": "application/json",
    "Accept" : "*/*"
}