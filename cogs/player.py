import discord
import requests
from discord.ext import commands
from utils import get_name_tag, is_nametag, get_color_from_image, get_rank_icon, get_rank_int_value, rgb, BLUE, RED, VALO_RED, GREEN, WIDTH
from main import get_nametag, check_request, get_rank_from_nametag, HEADERS

class PlayerCog(commands.Cog, name="Player"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command("player")
    async def get_player(self, ctx : commands.Context, nametag = None):
        """
        Displays information on a player
        """
        # Get data
        if nametag is None:
            real_nametag = get_nametag(ctx.author.id)
            if real_nametag is None:
                await ctx.send("You don't have a nametag linked to your account." \
                " Use `!player nametag` or `!setname nametag`")
                return
            else:
                nametag = real_nametag
        elif not is_nametag(nametag):
            await ctx.send("Invalid nametag format!")
            return
        name, tag = get_name_tag(nametag)
        response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", headers=HEADERS).json()
        if check_request(response):
            await ctx.send(check_request(response))
            return

        account_level = response["data"]["account_level"]
        card = response["data"]["card"]
        image = card["small"]
        color = get_color_from_image(card["small"])
        rank = get_rank_from_nametag(name,tag)
        if rank.startswith("Error"):
            await ctx.send(rank)
            return
        rank_icon = get_rank_icon(get_rank_int_value(rank))

        # Build embed
        embed = discord.Embed(
            description=f"## {name}#{tag}\n ### Level {account_level}",
            color=color
        )
        embed.add_field(name="Rank:", value=rank, inline=False)
        embed.set_thumbnail(url=rank_icon)
        embed.set_image(url=image)

        # Send embed
        await ctx.send(embed=embed)
    
    @commands.command(name="lastmach")
    async def get_last_match_leaderboard(self, ctx : commands.Context, nametag = None):
        """
        Displays a player's last match leaderboard
        """
        if nametag is None:
            real_nametag = get_nametag(ctx.author.id)
            if real_nametag is None:
                await ctx.send("You don't have a nametag linked to your account." \
                " Use `!player nametag` or `!setname nametag`")
                return
            else:
                nametag = real_nametag
        elif not is_nametag(nametag):
            await ctx.send("Invalid nametag format!")
            return
        name, tag = get_name_tag(nametag)
        response = requests.get(url=f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{name}/{tag}",headers=HEADERS).json()
        if check_request(response):
            await ctx.send(check_request(response))
            return

        last_match = response["data"][0]
        rounds = last_match["metadata"]["rounds_played"]
        players = last_match["players"]["all_players"]
        sorted_players = sorted(players, key=lambda x : x["stats"]["score"]//rounds,reverse=True)
        map = last_match["metadata"]["map"]
        mode = last_match["metadata"]["mode"]
        when = last_match["metadata"]["game_start_patched"]

        embeds = []
        winner = False
        for player in sorted_players:
            player_name = f'{player["name"]}#{player["tag"]}'
            score = player["stats"]["score"] // rounds
            k, d, a = player["stats"]["kills"], player["stats"]["deaths"], player["stats"]["assists"]
            player_team = player["team"]
            color = rgb(*VALO_RED) if player_team == "Red" else rgb(*BLUE) 
            if player_name.upper() == f"{name.upper()}#{tag.upper()}":
                winner = last_match["teams"][player_team.lower()]["has_won"]
                header = discord.Embed(
                    color=rgb(*GREEN) if winner else rgb(*RED),
                    description=f"## Map: {map}\n ## Mode: {mode}\n ## Date: {when}"
                )                

            embed =discord.Embed(
                    color=color,
                    description=f"### {player_name}",
                )
            embed.add_field(
                name="```Score```",
                value=f"{score}"
            )
            embed.add_field(
                name="```K/D/A```",
                value=f"{k}/{d}/{a}",
            )
            embed.set_thumbnail(
                url=player["assets"]["agent"]["small"]
            )
            embed.set_image(url=WIDTH)
            embeds.append(embed)

        await ctx.send(embed=header)
        await ctx.send(embeds=embeds)
    
async def setup(bot):
    await bot.add_cog(PlayerCog(bot))