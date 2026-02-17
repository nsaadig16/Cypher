import discord
import re
import requests
from colorthief import ColorThief
from discord.ext import commands
from io import BytesIO
from typing import Tuple

BLUE = (90, 200, 250)
VALO_RED = (255, 70, 85)
GREEN = (76, 187, 23)
RED = (255, 0, 0)

def get_color_from_image(url : str):
    response = requests.get(url)
    img = BytesIO(response.content)
    color_thief = ColorThief(img)
    r, g, b = color_thief.get_color(quality=1)
    return rgb(r,g,b)

def get_rank_icon(num : int):
    response = requests.get("https://valorant-api.com/v1/competitivetiers").json()
    return response["data"][-1]["tiers"][num]["smallIcon"]

def get_name_tag(nametag: Tuple[str, ...]):
    name_and_tag = "".join(nametag)
    return name_and_tag.strip().split("#")

def get_rank_int_value(rank: str):
    vals = {
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
        return 0
    elif tier == "RADIANT":
        return 27
    else:
        return vals[tier] + int(rank.split()[1])

def rgb(r, g, b):
    return (r << 16) + (g << 8) + b

def is_nametag(nametag):
    if re.match(r'[A-Za-z0-9]{3,16}\#[A-Za-z0-9]{3,5}', nametag):
        return True
    return False

class MyHelp(commands.DefaultHelpCommand):
    def get_category(self, command, *, default="General"):
        return default
    async def send_command_help(self, command):
        doc = command.callback.__doc__ or ""
        lines = [line.strip() for line in doc.splitlines()]

        description = []
        args = {}
        in_args = False

        for line in lines:
            if line.lower() == "arguments:":
                in_args = True
                continue

            if in_args:
                if ":" in line:
                    name, desc = line.split(":", 1)
                    args[name.strip()] = desc.strip()
            else:
                if line:
                    description.append(line)

        embed = discord.Embed(
            title=f"!{command.name}", description="\n".join(description)
        )

        for name, param in command.clean_params.items():
            desc = args.get(name, "No description")
            embed.add_field(name=name, value=desc, inline=False)

        await self.get_destination().send(embed=embed)