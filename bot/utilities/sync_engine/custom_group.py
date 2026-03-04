from typing import List
from discord import app_commands

REGISTERED_GROUPS: List[app_commands.Group] = []

def create_group(name: str, description: str) -> app_commands.Group:
    group = app_commands.Group(name=name, description=description)
    REGISTERED_GROUPS.append(group)
    return group