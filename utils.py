import re
import requests
from colorthief import ColorThief
from io import BytesIO
from typing import Tuple

BLUE = (90, 200, 250)
VALO_RED = (255, 70, 85)
GREEN = (76, 187, 23)
RED = (255, 0, 0)
WIDTH="https://i.sstatic.net/Fzh0w.png"

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
    return re.match(r'[A-Za-z0-9]{3,16}\#[A-Za-z0-9]{3,5}', nametag)
