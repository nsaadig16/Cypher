import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands
from utils import get_color_from_image

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
async def player(ctx, *args):
    name_and_tag = ''.join(args)
    name, tag = name_and_tag.strip().split('#')
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", headers=headers).json()
    account_level = response["data"]["account_level"]
    card = response["data"]["card"]
    image = card["small"]
    color = get_color_from_image(card["small"])
    rank = get_rank_from_nametag(name,tag)
    embed = discord.Embed(
        #title=f"=========",
        description=f"## {name}#{tag} \n**Level {account_level}**",
        color=color,
    )
    embed.add_field(name="Current rank (EU):", value=rank, inline=False)

    embed.set_thumbnail(
        url=image
    )
    await ctx.send(embed=embed)

def get_rank_from_nametag(name, tag):
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v3/mmr/eu/pc/{name}/{tag}", headers=headers).json()
    return response["data"]["current"]["tier"]["name"]

bot.run(token=token)
