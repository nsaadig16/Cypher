from discord.ext import commands
from main import Cypher

class UtilityCog(commands.Cog, name="Utility"):
    def __init__(self, bot : Cypher):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx : commands.Context):
        """
        Responds with "Pong!"
        """
        await ctx.send("Pong!")

    @commands.command(name="isup")
    async def is_up(self, ctx : commands.Context):
        """
        Checks if the server for the Europe region is up.
        """
        response = await self.bot.fetch(f"https://api.henrikdev.xyz/valorant/v1/status/{self.bot.REGION}")
        is_up = response["status"]

        # Check status code
        if is_up == 200:
            await ctx.send("The server for the Europe region is up!")
        else:
            await ctx.send("The server for the Europe region is down!")
    
        
    
async def setup(bot):
    await bot.add_cog(UtilityCog(bot))