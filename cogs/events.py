from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from main import Cypher

class EventCog(commands.Cog, name="Events"):
    def __init__(self, bot : Cypher):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cypher's in!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("❌ Command not found.\nUse `!help` to see available commands.")
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(
                f"❌ Missing required argument: `{error.param.name}`.\nUse `!help {ctx.command}` for usage info."
            )
        raise error
    
async def setup( bot):
    await bot.add_cog(EventCog(bot))