import aiohttp
import aiosqlite
from cypher.config import TOKEN, HEADERS, DB_PATH
from discord import Intents
from discord.ext.commands import Bot
from pathlib import Path
from typing import override

class Cypher(Bot):
    def __init__(self, db_name, headers, intents, region = "eu"):
        super().__init__(command_prefix="!", intents=intents)
        self.HEADERS = headers
        self.REGION = region
        self.DB_NAME = db_name
    
    @override
    async def setup_hook(self):
        self.session = aiohttp.ClientSession(headers=self.HEADERS)
        self.conn = await aiosqlite.connect(self.DB_NAME)
        cogs_path = Path(__file__).parent / "cogs"
        cogs = [f.stem for f in cogs_path.iterdir() if f.suffix == ".py" and f.name != "__init__.py"]
        for cog in cogs:
            await self.load_extension(f'cypher.cogs.{cog}')

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

def main():
    if not all([TOKEN, HEADERS, DB_PATH]):
        print("Environment variables not set.\n" \
        "Make sure you have your bot's TOKEN and your HenrikDev API key!")
        exit()
    intents = Intents.default()
    intents.message_content = True
    bot = Cypher(DB_PATH, HEADERS, intents)
    bot.run(token=TOKEN)

if __name__=="__main__":
    main()