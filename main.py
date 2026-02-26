import aiohttp
import discord
import os
import aiosqlite
from dotenv import load_dotenv
from discord.ext.commands import Bot
from typing import override


class Cypher(Bot):
    def __init__(self, db_name, headers, region = "eu"):
        super().__init__(command_prefix="!", intents=intents)
        self.HEADERS = headers
        self.REGION = region
        self.DB_NAME = db_name
    
    @override
    async def setup_hook(self):
        self.session = aiohttp.ClientSession(headers=self.HEADERS)
        self.conn = await aiosqlite.connect(self.DB_NAME)
        self.c = self.conn.cursor()
        cogs = [s.removesuffix(".py") for s in os.listdir("cogs") if s.endswith(".py")]
        for cog in cogs:
            await self.load_extension(f'cogs.{cog}')

    @override
    async def close(self):
        await self.session.close()
        await self.conn.close()
        await super().close()
    
    async def fetch(self, url):
        async with self.session.get(url) as resp:
            return await resp.json()

def check_request(response):
    if response.get("errors",False):
        message = response["errors"][0]["message"]
        return f"Error: {message}"
    return None

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
    bot = Cypher(DB_NAME, HEADERS)
    bot.run(token=TOKEN)