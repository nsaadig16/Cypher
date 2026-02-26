from discord.ext import commands
import discord

class HelpCog(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = None  # disable default help

    @commands.command(name="help")
    async def help(self, ctx, command_name=None):
        """Shows all available commands."""
        if command_name:
            command = self.bot.get_command(command_name)
            if command is None:
                await ctx.send(f"❌ Command `{command_name}` not found.")
                return
            embed = discord.Embed(
                title=f"!{command.name} {command.signature}",
                description=command.help or "No description provided.",
                color=discord.Color.blurple(),
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Commands", color=discord.Color.blurple())
        for cog_name, cog in self.bot.cogs.items():
            cog_commands = cog.get_commands()
            if not cog_commands:
                continue
            embed.add_field(
                name=cog_name,
                value="\n".join(
                    f"`!{cmd.name} {cmd.signature}` — {cmd.help or 'No description'}"
                    for cmd in cog_commands
                ),
                inline=False,
            )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
