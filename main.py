import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
from utils import get_color_from_image, get_rank_icon

load_dotenv()
token = os.getenv("TOKEN","")
api_key = os.getenv("API_KEY","")

headers = {
    "Authorization" : api_key,
    "Content-Type": "application/json",
    "Accept" : "*/*"
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Cypher's in!")

@bot.command()
async def test(ctx, *args):
    await ctx.send(f"You said {' '.join(args)}")

@bot.command()
async def is_up(ctx):
    region = "eu"
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/status/{region}", headers=headers).json()
    is_up = response["status"]

    if is_up == 200:
        await ctx.send("The server for the Europe region is up!")
    else:
        await ctx.send("The server for the Europe region is down!")

@bot.command()
async def player(ctx, *nametag):
    name_and_tag = ''.join(nametag)
    name, tag = name_and_tag.strip().split('#')
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", headers=headers).json()
    account_level = response["data"]["account_level"]
    card = response["data"]["card"]
    image = card["small"]
    color = get_color_from_image(card["small"])
    rank = get_rank_from_nametag(name,tag)
    rank_icon = get_rank_icon(get_rank_int_value(rank))

    embed = discord.Embed(
        description=f"## {name}#{tag}\n ### Level {account_level}",
        color=color
    )
    embed.add_field(name="Rank:", value=rank, inline=False)
    embed.set_thumbnail(url=rank_icon)
    embed.set_image(url=image)

    await ctx.send(embed=embed)

def get_rank_from_nametag(name, tag):
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v3/mmr/eu/pc/{name}/{tag}", headers=headers).json()
    return response["data"]["current"]["tier"]["name"].upper()

def get_rank_int_value(rank : str):
    print(rank)
    vals = {"IRON" : 2, "BRONZE" : 5, "SILVER" : 8,
            "GOLD" : 11, "PLATINUM" : 14, "DIAMOND" : 17, "ASCENDANT" : 20, "IMMORTAL" : 23,
    }
    tier = rank.split()[0]
    print(f"tier {tier}")
    if tier == "UNRATED":
        return 0
    elif tier == "RADIANT":
        return 27
    else:
        return vals[tier] + int(rank.split()[1])

bot.run(token=token)
