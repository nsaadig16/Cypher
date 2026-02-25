from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from utils import is_nametag
from db.db import insert_nametag, get_nametag_from_id, remove_nametag

class ProfileCog(commands.Cog, name="Profile"):
    def __init__(self, bot):
        self.bot = bot
        self.conn, self.c = bot.conn, bot.c

    @commands.command(name = "setname")
    async def set_name(self, ctx : commands.Context, nametag):
        """
        Link a nametag to your user
        """
        if not is_nametag(nametag):
            await ctx.send("Invalid nametag format!")
            return
        id = ctx.author.id
        insert_nametag(self.conn, self.c, id, nametag)
        self.bot.conn.commit()
        await ctx.send(f"Successfuly linked the nametag {nametag} to your user!")

    
    @commands.command(name= "showname")
    async def show_name(self, ctx: commands.Context):
        """
        Show the nametag linked to your user
        """
        id = ctx.author.id
        row = get_nametag_from_id(self.conn, self.c, id)
        if row is None:
            await ctx.send("You don't have a nametag stored. Do it using `!setname`")
        else:
            nametag = row[0]
            await ctx.send(f"Your username is `{nametag}`")
    
    @commands.command(name= "removename")
    async def remove_name(self, ctx: commands.Context):
        """
        Delete the nametag linked to your user
        """
        id = ctx.author.id
        delete_outcome = remove_nametag(self.conn, self.c, id)
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