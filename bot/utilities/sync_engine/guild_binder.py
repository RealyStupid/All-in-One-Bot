import discord
from discord.ext import commands
from discord import app_commands

from utilities.db_manager.db_manager import get_enabled_modules_for_guild
from utilities.custom_command_api.registry import (
    GLOBAL_COMMAND_DEFS,
    MODULE_COMMAND_DEFS,
    GROUP_DEFS,
    STANDALONE_GLOBAL_COMMAND_DEFS,
    STANDALONE_MODULE_COMMAND_DEFS,
)
from utilities.custom_command_api.builder import (
    build_command,
)


# ---------------------------------------------------------
# GLOBAL SYNC
# ---------------------------------------------------------
async def sync_global(bot: commands.Bot):
    tree = bot.tree

    # Clear existing global commands on Discord
    tree.clear_commands(guild=None)

    global_commands = []

    # Standalone GLOBAL commands
    for defn in STANDALONE_GLOBAL_COMMAND_DEFS:
        global_commands.append(build_command(defn))

    # Grouped GLOBAL commands
    for defn in GLOBAL_COMMAND_DEFS:
        global_commands.append(build_command(defn))

    # Global groups
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
            new_group.add_command(build_command(sub_def))

        global_commands.append(new_group)

    # Add commands to tree
    for cmd in global_commands:
        tree.add_command(cmd)

    synced = await tree.sync()
    print(f"[SYNC ENGINE] Synced GLOBAL commands: {len(synced)}")
    return synced


# ---------------------------------------------------------
# GUILD SYNC
# ---------------------------------------------------------
async def rebuild_commands_for_guild(bot: commands.Bot, guild_id: int):
    tree: app_commands.CommandTree = bot.tree
    guild_obj = discord.Object(id=guild_id)

    enabled_modules = await get_enabled_modules_for_guild(guild_id)

    commands_for_guild = []

    # Standalone GLOBAL commands
    for defn in STANDALONE_GLOBAL_COMMAND_DEFS:
        commands_for_guild.append(build_command(defn))

    # Standalone MODULE commands
    for defn in STANDALONE_MODULE_COMMAND_DEFS:
        if defn.module in enabled_modules:
            commands_for_guild.append(build_command(defn))

    # Grouped GLOBAL commands
    for defn in GLOBAL_COMMAND_DEFS:
        commands_for_guild.append(build_command(defn))

    # Grouped MODULE commands
    for defn in MODULE_COMMAND_DEFS:
        if defn.module in enabled_modules:
            commands_for_guild.append(build_command(defn))

    # Groups
    for group_def in GROUP_DEFS:
        allowed_subs = [
            sub for sub in group_def.subcommands
            if sub.module in enabled_modules
        ]

        if not allowed_subs:
            continue

        new_group = app_commands.Group(
            name=group_def.name,
            description=group_def.description
        )

        for sub_def in allowed_subs:
            new_group.add_command(build_command(sub_def))

        commands_for_guild.append(new_group)

    # Clear & re-add
    tree.clear_commands(guild=guild_obj)

    for cmd in commands_for_guild:
        tree.add_command(cmd, guild=guild_obj)

    names = [cmd.qualified_name for cmd in commands_for_guild]
    print(f"[SYNC ENGINE] Rebuilt commands for guild {guild_id}: {len(commands_for_guild)} -> {names}")


async def sync_guild(bot: commands.Bot, guild_id: int):
    await rebuild_commands_for_guild(bot, guild_id)
    guild_obj = discord.Object(id=guild_id)
    synced = await bot.tree.sync(guild=guild_obj)
    print(f"[SYNC ENGINE] Synced guild {guild_id}: {len(synced)} commands.")
    return synced