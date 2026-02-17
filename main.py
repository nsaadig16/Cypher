import discord
import requests
import os
import sqlite3
import utils
from dotenv import load_dotenv
from discord.ext.commands import Bot, Context, CommandNotFound
from utils import RED, GREEN, VALO_RED, BLUE

load_dotenv()
TOKEN = os.getenv("TOKEN","")
API_KEY = os.getenv("API_KEY","")
DB_NAME = "db/players.db"
HEADERS = {
    "Authorization" : API_KEY,
    "Content-Type": "application/json",
    "Accept" : "*/*"
}
REGION = "eu"

intents = discord.Intents.default()
intents.message_content = True
bot = Bot(command_prefix="!", intents=intents)
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

@bot.event
async def on_ready():
    print("Cypher's in!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("❌ Command not found.\nUse `!help` to see available commands.")
        return
    raise error


@bot.command(name="ping")
async def ping(ctx : Context):
    """
    Responds with "Pong!"
    """
    await ctx.send("Pong!")

@bot.command(name="isup")
async def is_up(ctx : Context):
    """
    Checks if the server for the Europe region is up.
    """
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/status/{REGION}", headers=HEADERS).json()
    is_up = response["status"]

    # Check status code
    if is_up == 200:
        await ctx.send("The server for the Europe region is up!")
    else:
        await ctx.send("The server for the Europe region is down!")

@bot.command(name="player")
async def get_player(ctx : Context, nametag):
    """
    Displays information on a player

    Arguments:
        nametag: the player's nametag
    """
    # Get data
    if not utils.is_nametag(nametag):
        await ctx.send("Invalid nametag format!")
        return
    name, tag = utils.get_name_tag(nametag)
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}", headers=HEADERS).json()
    if check_request(response):
        await ctx.send(check_request(response))
        return

    account_level = response["data"]["account_level"]
    card = response["data"]["card"]
    image = card["small"]
    color = utils.get_color_from_image(card["small"])
    rank = get_rank_from_nametag(name,tag)
    if rank.startswith("Error"):
        await ctx.send(rank)
        return
    rank_icon = utils.get_rank_icon(utils.get_rank_int_value(rank))

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
async def get_last_match_leaderboard(ctx : Context, nametag):
    """
    Displays a player's last match leaderboard

    Arguments:
        nametag: the player's nametag
    """
    if not utils.is_nametag(nametag):
        await ctx.send("Invalid nametag format!")
        return
    name, tag = utils.get_name_tag(nametag)
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
        player_name = f"{player["name"]}#{player["tag"]}"
        score = player["stats"]["score"] // rounds
        k, d, a = player["stats"]["kills"], player["stats"]["deaths"], player["stats"]["assists"]
        player_team = player["team"]
        color = utils.rgb(*VALO_RED) if player_team == "Red" else utils.rgb(*BLUE) 
        print(f"plnm='{player_name}',nt='{name}#{tag}'")
        if player_name.upper() == f"{name.upper()}#{tag.upper()}":
            winner = last_match["teams"][player_team.lower()]["has_won"]
            print("dadakslkap")
            header = discord.Embed(
                color=utils.rgb(*GREEN) if winner else utils.rgb(*RED),
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
        embed.set_image(url="https://i.sstatic.net/Fzh0w.png")
        embeds.append(embed)

    await ctx.send(embed=header)
    await ctx.send(embeds=embeds)

@bot.command(name="setname")
async def set_name(ctx : Context, nametag):
    """
    Link a nametag to your user

    Arguments:
        nametag: your nametag
    """
    if not utils.is_nametag(nametag):
        await ctx.send("Invalid nametag format!")
        return
    id = ctx.author.id
    c.execute(
        "INSERT OR REPLACE INTO users (id, nametag) VALUES (?,?)",
        (id,nametag)
    )
    conn.commit()
    await ctx.send(f"Successfuly linked the nametag {nametag} to your user!")

@bot.command(name="getname")
async def get_name(ctx: Context):
    """
    Show the nametag linked to your user
    """
    id = ctx.author.id
    c.execute("SELECT nametag FROM users WHERE id = ?",
              (id,)
    )
    row = c.fetchone()
    if row is None:
        await ctx.send("You don't have a nametag stored. Do it using `!setname`")
    else:
        nametag = row[0]
        await ctx.send(f"Your username is `{nametag}`")

@bot.command(name="removename")
async def remove_name(ctx: Context):
    """
    Delete the nametag linked to your user
    """
    id = ctx.author.id
    c.execute("DELETE FROM users WHERE id = ?", (id,))
    if c.rowcount == 0:
        await ctx.send("You don't have a nametag stored. Do it using `!setname`")
    else:
        conn.commit()
        await ctx.send("Deleted nametag for your user!")

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
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nametag TEXT NOT NULL
        )
        """
    )
    bot.help_command = utils.MyHelp()
    bot.run(token=TOKEN)