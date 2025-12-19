import re

from enum import Enum


class NutCommand(Enum):
    ListUps = "LIST UPS"
    ListVar = "LIST VAR"


NUT_COMMANDS_RE = re.compile(
    r"^(?P<cw>LIST\sUPS)|(?P<ca>LIST\sVAR)\s(?P<a>[A-Za-z0-9]+)$",
)
"""
Groups:\n
cw - cmd without args\n
ca - cmd with args\n
a - cmd args
"""
