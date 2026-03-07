import discord
from discord.ext import commands
from discord import app_commands

from utilities.db_manager.db_manager import GUILD_IDS, get_enabled_modules_for_guild
from utilities.sync_engine.custom_group import REGISTERED_GROUPS


async def rebuild_commands_for_guild(bot: commands.Bot, guild_id: int):
    tree: app_commands.CommandTree = bot.tree
    guild_obj = discord.Object(id=guild_id)

    enabled_modules = await get_enabled_modules_for_guild(guild_id)

    commands_for_guild: list[app_commands.Command | app_commands.Group] = []

    # ---------------------------------------------------------
    # 1) NORMAL COMMANDS (leaf commands)
    # ---------------------------------------------------------
    for command in tree.walk_commands():

        # Skip groups — handled separately
        if isinstance(command, app_commands.Group):
            continue

        callback = getattr(command, "callback", None)
        if callback is None:
            continue

        # GLOBAL COMMANDS HAVE NO MODULE
        module_name = getattr(callback, "__module_name__", None)

        # Skip global commands (they stay global)
        if module_name is None:
            continue

        # Skip commands whose module is disabled
        if module_name not in enabled_modules:
            continue

        commands_for_guild.append(command)

    # ---------------------------------------------------------
    # 2) CUSTOM GROUPS (from REGISTERED_GROUPS)
    # ---------------------------------------------------------
    for group in REGISTERED_GROUPS:

        allowed_subcommands: list[app_commands.Command] = []

        for sub in group.commands:
            callback = getattr(sub, "callback", None)
            if callback is None:
                continue

            module_name = getattr(callback, "__module_name__", None)

            # Skip global subcommands
            if module_name is None:
                continue

            # Skip disabled modules
            if module_name not in enabled_modules:
                continue

            allowed_subcommands.append(sub)

        # If no subcommands allowed → skip entire group
        if not allowed_subcommands:
            continue

        # Rebuild the group fresh for this guild
        new_group = app_commands.Group(
            name=group.name,
            description=group.description
        )

        for sub in allowed_subcommands:
            new_group.add_command(sub)

        commands_for_guild.append(new_group)

    # ---------------------------------------------------------
    # 3) CLEAR & RE-ADD COMMANDS FOR THIS GUILD
    # ---------------------------------------------------------
    tree.clear_commands(guild=guild_obj)

    for cmd in commands_for_guild:
        tree.add_command(cmd, guild=guild_obj)

    names = [cmd.qualified_name for cmd in commands_for_guild]
    print(f"[SYNC ENGINE] Rebuilt commands for guild {guild_id}: {len(commands_for_guild)} commands -> {names}")


async def sync_guild(bot: commands.Bot, guild_id: int):
    await rebuild_commands_for_guild(bot, guild_id)
    guild_obj = discord.Object(id=guild_id)
    synced = await bot.tree.sync(guild=guild_obj)
    print(f"[SYNC ENGINE] Synced guild {guild_id}: {len(synced)} commands.")
    return synced


async def sync_all_registered_guilds(bot: commands.Bot):
    total = 0
    for gid in GUILD_IDS:
        synced = await sync_guild(bot, gid)
        total += len(synced)

    print(f"[SYNC ENGINE] Finished syncing all registered guilds. Total commands synced: {total}")
    return total


async def unsync_guild(bot, guild_id: int):
    guild = bot.get_guild(guild_id)
    if guild:
        await bot.tree.sync(guild=guild)