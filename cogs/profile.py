from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from utils import check_nametag, NametagFormatException
from db.db import insert_nametag, get_nametag_from_id, remove_nametag
from main import Cypher

class ProfileCog(commands.Cog, name="Profile"):
    def __init__(self, bot : Cypher):
        self.bot = bot
        self.conn = bot.conn

    @commands.command(name = "setname")
    async def set_name(self, ctx : commands.Context, nametag):
        """
        Link a nametag to your user
        """
        try:
            check_nametag(nametag)
        except NametagFormatException as e:
            await ctx.send(f"Error: {e}")
            return
        id = ctx.author.id
        await insert_nametag(self.conn, id, nametag)
        await ctx.send(f"Successfuly linked the nametag {nametag} to your user!")

    
    @commands.command(name= "showname")
    async def show_name(self, ctx: commands.Context):
        """
        Show the nametag linked to your user
        """
        id = ctx.author.id
        row = await get_nametag_from_id(self.conn, id)
        if row is None:
            await ctx.send("You don't have a nametag stored. Do it using `!setname`")
        else:
            nametag = row #pyright: ignore
            await ctx.send(f"Your username is `{nametag}`")
    
    @commands.command(name= "removename")
    async def remove_name(self, ctx: commands.Context):
        """
        Delete the nametag linked to your user
        """
        id = ctx.author.id
        delete_outcome = await remove_nametag(self.conn, id)
        if not delete_outcome:
            await ctx.send("You don't have a nametag stored. Do it using `!setname`")
        else:
            await ctx.send("Deleted nametag for your user!")

    @set_name.error
    async def set_name_error(self, ctx: commands.Context, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("❌ Please provide your nametag.\nUsage: `!setname Name#TAG`")
    
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))