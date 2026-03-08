import discord
from discord.ext import commands
from discord import app_commands

from utilities.custom_command_api.registry import (
    GLOBAL_COMMAND_DEFS,
    GROUP_DEFS,
    STANDALONE_GLOBAL_COMMAND_DEFS,
)
from utilities.custom_command_api.builder import build_command


async def register_global_commands(bot: commands.Bot):
    """
    Build and register global commands into bot.tree so Discord.py
    can execute them when interactions arrive.

    This does NOT sync to Discord - it only registers in memory.
    """
    tree: app_commands.CommandTree = bot.tree

    # Clear any existing global commands in memory (not on Discord)
    tree.clear_commands(guild=None)

    global_count = 0

    # ---------------------------------------------------------
    # Standalone GLOBAL commands
    # ---------------------------------------------------------
    for defn in STANDALONE_GLOBAL_COMMAND_DEFS:
        cmd = build_command(defn)
        tree.add_command(cmd)
        global_count += 1

    # ---------------------------------------------------------
    # Grouped GLOBAL commands
    # ---------------------------------------------------------
    for defn in GLOBAL_COMMAND_DEFS:
        cmd = build_command(defn)
        tree.add_command(cmd)
        global_count += 1

    # ---------------------------------------------------------
    # Global groups (only subcommands where module=None)
    # ---------------------------------------------------------
    for group_def in GROUP_DEFS:
        allowed_subs = [
            sub for sub in group_def.subcommands
            if sub.module is None
        ]

        if not allowed_subs:
            continue

        new_group = app_commands.Group(
            name=group_def.name,
            description=group_def.description
        )

        for sub_def in allowed_subs:
            sub_cmd = build_command(sub_def)
            new_group.add_command(sub_cmd)

        tree.add_command(new_group)
        global_count += 1

    print(f"[EXECUTION MANAGER] Registered {global_count} global commands/groups for execution.")