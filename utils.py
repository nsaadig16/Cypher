import requests
from colorthief import ColorThief
from io import BytesIO

def get_color_from_image(url : str):
    response = requests.get(url)
    img = BytesIO(response.content)
    color_thief = ColorThief(img)
    r, g, b = color_thief.get_color(quality=1)
    return (r << 16) + (g << 8) + b

def get_rank_icon( num : int):
    response = requests.get("https://valorant-api.com/v1/competitivetiers").json()
    return response["data"][-1]["tiers"][num]["smallIcon"]