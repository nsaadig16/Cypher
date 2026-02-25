import aiohttp
import discord
import os
import sqlite3
from dotenv import load_dotenv
from discord.ext.commands import Bot
from typing import override


class Cypher(Bot):
    def __init__(self, db_name, headers, region = "eu"):
        super().__init__(command_prefix="!", intents=intents)
        self.HEADERS = headers
        self.REGION = region
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
    
    @override
    async def setup_hook(self):
        self.session = aiohttp.ClientSession(headers=self.HEADERS)
        cogs = [s.removesuffix(".py") for s in os.listdir("cogs") if s.endswith(".py")]
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')

    @override
    async def close(self):
        await self.session.close()
        self.conn.close()
        await super().close()
    
    async def fetch(self, url):
        async with self.session.get(url) as resp:
            return await resp.json()

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
    intents = discord.Intents.default()
    intents.message_content = True
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    bot = Cypher(DB_NAME, HEADERS)
    bot.run(token=TOKEN)