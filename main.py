import discord
import json
import requests
import os
from dotenv import load_dotenv
from discord.ext import commands

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
    await ctx.send(f"You said {args}")

@bot.command()
async def is_up(ctx):
    region = "eu"
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/status/{region}", headers=headers).json()
    is_up = response["status"]

    if is_up == 200:
        await ctx.send("The server for this region is up!")
    else:
        await ctx.send("The server for this region is down!")



bot.run(token=token)
