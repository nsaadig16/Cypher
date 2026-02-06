import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
from utils import get_color_from_image, get_rank_icon, get_name_tag, get_rank_int_value, rgb

load_dotenv()
TOKEN = os.getenv("TOKEN","")
API_KEY = os.getenv("API_KEY","")
HEADERS = {
    "Authorization" : API_KEY,
    "Content-Type": "application/json",
    "Accept" : "*/*"
}
BLUE = (90, 200, 250)
RED = (255, 70, 85)
REGION = "eu"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Cypher's in!")

@bot.command()
async def is_up(ctx):
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/status/{REGION}", headers=HEADERS).json()
    is_up = response["status"]

    # Check status code
    if is_up == 200:
        await ctx.send("The server for the Europe region is up!")
    else:
        await ctx.send("The server for the Europe region is down!")

@bot.command(name="player")
async def get_player(ctx, *nametag):
    # Get data
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

@bot.command(name='lastmatch')
async def get_last_match_leaderboard(ctx, *nametag):
    # Get data
    name, tag = get_name_tag(nametag)
    response = requests.get(url=f"https://api.henrikdev.xyz/valorant/v3/matches/eu/{name}/{tag}",headers=HEADERS).json()
    if check_request(response):
        await ctx.send(check_request(response))
        return

    last_match = response["data"][0]
    rounds = last_match["metadata"]["rounds_played"]
    players = last_match["players"]["all_players"]
    sorted_players = sorted(players, key=lambda x : x["stats"]["score"]//rounds,reverse=True)

    embeds = []
    for player in sorted_players:
        player_name = f"{player["name"]}#{player["tag"]}"
        score = player["stats"]["score"] // rounds
        k, d, a = player["stats"]["kills"], player["stats"]["deaths"], player["stats"]["assists"]
        color = rgb(*RED) if player["team"] == "Red" else rgb(*BLUE) 

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
        embed.set_image(url="https://i.sstatic.net/Fzh0w.png")
        embeds.append(embed)
    await ctx.send(embeds=embeds)

def get_rank_from_nametag(name, tag):
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v3/mmr/eu/pc/{name}/{tag}", headers=HEADERS).json()
    if response.get("errors",False):
        message = response["errors"][0]["message"]
        return "Error: " + message
    return response["data"]["current"]["tier"]["name"].upper()

def check_request(response):
    if response.get("errors",False):
        message = response["errors"][0]["message"]
        return f"Error: {message}"
    return None

if __name__ == "__main__": 
    bot.run(token=TOKEN)
