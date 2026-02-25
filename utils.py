import re
from typing import Tuple

BLUE = (90, 200, 250)
VALO_RED = (255, 70, 85)
GREEN = (76, 187, 23)
RED = (255, 0, 0)
WIDTH="https://i.sstatic.net/Fzh0w.png"

def get_name_tag(nametag: Tuple[str, ...]):
    name_and_tag = "".join(nametag)
    return name_and_tag.strip().split("#")

def rgb(r, g, b):
    return (r << 16) + (g << 8) + b

def is_nametag(nametag):
    nametag_regex = (r"[A-Za-z0-9]{3,16}\#[A-Za-z0-9]{3,5}")
    return re.match(nametag_regex, nametag)
