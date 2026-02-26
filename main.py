import aiohttp
import aiosqlite
import os
from config import TOKEN, HEADERS, DB_NAME
from discord import Intents
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
    
    async def fetch_bytes(self, url):
        async with self.session.get(url) as resp:
            return await resp.read()

if __name__ == "__main__":
    if not all([TOKEN, HEADERS, DB_NAME]):
        print("Environment variables not set.\n" \
        "Make sure you have your bot's TOKEN and your HenrikDev API key!")
        exit()
    intents = Intents.default()
    intents.message_content = True
    bot = Cypher(DB_NAME, HEADERS)
    bot.run(token=TOKEN)