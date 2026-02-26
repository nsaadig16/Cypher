import re
from typing import Tuple, Union
from cypher.exceptions import NametagFormatException, APIException

COLORS ={
    "RED" : (255, 0, 0),
    "VALO_BLUE" : (90, 200, 250),
    "GREEN" : (76, 187, 23),
    "VALO_RED" : (255, 70, 85)
}
WIDE_IMAGE = "https://i.sstatic.net/Fzh0w.png"

def get_name_tag(nametag: Union[Tuple, str]):
    name_and_tag = "".join(nametag)
    return name_and_tag.strip().split("#")

def rgb(r, g, b):
    return (r << 16) + (g << 8) + b

def check_nametag(nametag):
    nametag_regex = (r"[A-Za-z0-9]{3,16}\#[A-Za-z0-9]{3,5}")
    if not re.match(nametag_regex, nametag):
        raise NametagFormatException("Invalid nametag format!")

def check_request(response):
    if response.get("errors", False):
        message = response["errors"][0]["message"]
        raise APIException(message)

