from discord import Embed
from colorthief import ColorThief
from discord.ext import commands
from cypher.db.db import get_nametag_from_id
from cypher.exceptions import NametagNotStoredException, APIException
from io import BytesIO
from cypher.utils import get_name_tag, check_nametag, rgb, check_request, COLORS, WIDE_IMAGE
from cypher.main import Cypher

class PlayerCog(commands.Cog, name="Player"):
    def __init__(self, bot : Cypher):
        self.bot = bot
    
    @commands.command("player")
    async def get_player(self, ctx : commands.Context, nametag : str | None = None):
        """
        Displays information on a player
        """
        try:
            name, tag = await self.process_nametag(ctx, nametag)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            return
        
        try:
            response = await self.bot.fetch(
                    f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
            )
            check_request(response)
        except APIException as e:
            await ctx.send(f"Error: {e}")
            return
    
        account_level = response["data"]["account_level"]
        card = response["data"]["card"]
        image = card["small"]
        color = await self.get_color_from_image(card["small"])
        rank = await self._get_rank_from_nametag(name,tag)
        if rank.startswith("Error"):
            await ctx.send(rank)
            return
        rank_icon = await self.get_rank_icon(rank)

        # Build embed
        embed = Embed(
            description=f"## {name}#{tag}\n ### Level {account_level}",
            color=color
        )
        embed.add_field(name="Rank:", value=rank, inline=False)
        embed.set_thumbnail(url=rank_icon)
        embed.set_image(url=image)

        # Send embed
        await ctx.send(embed=embed)
    
    
    @commands.command(name="lastmatch")
    async def get_last_match_leaderboard(self, ctx : commands.Context, nametag : str | None = None):
        """
        Displays a player's last match leaderboard
        """
        try:
            name, tag = await self.process_nametag(ctx, nametag)
        except Exception as e:
            await ctx.send(f"Error: {e}")
            return
        
        try:
            response = await self.bot.fetch(url=f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{name}/{tag}")
            check_request(response)
        except APIException as e:
            await ctx.send(f"Error: {e}")
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
            color = rgb(*COLORS["VALO_RED"]) if player_team == "Red" else rgb(*COLORS["VALO_BLUE"]) 
            if player_name.upper() == f"{name.upper()}#{tag.upper()}":
                winner = last_match["teams"][player_team.lower()]["has_won"]
                header = Embed(
                    color=rgb(*COLORS["GREEN"]) if winner else rgb(*COLORS["RED"]),
                    description=f"## Map: {map}\n ## Mode: {mode}\n ## Date: {when}"
                )                

            embed = Embed(
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
            embed.set_image(url=WIDE_IMAGE)
            embeds.append(embed)

        await ctx.send(embed=header)
        await ctx.send(embeds=embeds)
    
    # ====================
    # Utility functions
    # ====================

    async def _get_rank_from_nametag(self, name : str, tag : str):
        response = await self.bot.fetch(f"https://api.henrikdev.xyz/valorant/v3/mmr/eu/pc/{name}/{tag}")
        if response.get("errors",False):
            message = response["errors"][0]["message"]
            return "Error: " + message
        return response["data"]["current"]["tier"]["name"].upper()

    async def get_rank_icon(self, rank : str):
        tiers = {
            "IRON": 2,
            "BRONZE": 5,
            "SILVER": 8,
            "GOLD": 11,
            "PLATINUM": 14,
            "DIAMOND": 17,
            "ASCENDANT": 20,
            "IMMORTAL": 23,
        }
        tier = rank.split()[0]
        if tier == "UNRATED":
            num = 0
        elif tier == "RADIANT":
            num = 27
        else:
            num = tiers[tier] + int(rank.split()[1])
        response = await self.bot.fetch("https://valorant-api.com/v1/competitivetiers")
        return response["data"][-1]["tiers"][num]["smallIcon"]

    async def get_color_from_image(self, url : str):
        response = await self.bot.fetch_bytes(url)
        img = BytesIO(response)
        color_thief = ColorThief(img)
        r, g, b = color_thief.get_color(quality=1)
        return rgb(r,g,b)

    async def process_nametag(self, ctx, nametag):
        if nametag is None:
            db_nametag = await get_nametag_from_id(self.bot.conn, ctx.author.id)
            if db_nametag is None:                
                raise NametagNotStoredException("You don't have a nametag linked to your account." \
                    " Use `!player nametag` or `!setname nametag`"
                )
            else:
                real_nametag = db_nametag
        else:
            real_nametag = nametag
        check_nametag(real_nametag)
        name, tag = get_name_tag(real_nametag)
        return name, tag

async def setup(bot):
    await bot.add_cog(PlayerCog(bot))