import discord
import requests
import os
import sqlite3
from dotenv import load_dotenv
from discord.ext.commands import Bot
from typing import override


class Cypher(Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.conn = sqlite3.connect(DB_NAME)
        self.c = conn.cursor()
        self.bot = self
    
    @override
    async def setup_hook(self):
        cogs = [s.removesuffix(".py") for s in os.listdir("cogs") if s.endswith(".py")]
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')

    @override
    async def close(self):
        self.conn.close()

def get_rank_from_nametag(name, tag):
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v3/mmr/eu/pc/{name}/{tag}", headers=HEADERS).json()
    if response.get("errors",False):
        message = response["errors"][0]["message"]
        return "Error: " + message
    return response["data"]["current"]["tier"]["name"].upper()

def check_request(response):
    if response.get("errors",False):
        message = response["errors"][0]["message"]
        return f"Error: {message}"
    return None

def get_nametag(id : int):
    c.execute("SELECT nametag FROM users WHERE id = ?",
              (id,)
    )
    row = c.fetchone()
    if row is None:
        return None
    else:
        return row[0]

if __name__ == "__main__":
    
    if not load_dotenv():
        print("Environment variables not set.\n" \
        "Make sure you have your bot's TOKEN and your HenrikDev API key!")
        exit()
    TOKEN = os.getenv("TOKEN","")
    API_KEY = os.getenv("API_KEY","")
    DB_NAME = "db/players.db"
    HEADERS = {
        "Authorization" : API_KEY,
        "Content-Type": "application/json",
        "Accept" : "*/*"
    }
    REGION = "eu"
    intents = discord.Intents.default()
    intents.message_content = True
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    bot = Cypher()
    bot.run(token=TOKEN)