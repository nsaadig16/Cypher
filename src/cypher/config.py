import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv("TOKEN","")
API_KEY = os.getenv("API_KEY","")
DB_PATH = Path(__file__).parent / "db" / "players.db"
HEADERS = {
    "Authorization" : API_KEY,
    "Content-Type": "application/json",
    "Accept" : "*/*"
}