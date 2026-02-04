import requests
from colorthief import ColorThief
from io import BytesIO

def get_color_from_image(url : str):
    response = requests.get(url)
    img = BytesIO(response.content)
    color_thief = ColorThief(img)
    r, g, b = color_thief.get_color(quality=1)
    return (r << 16) + (g << 8) + b
