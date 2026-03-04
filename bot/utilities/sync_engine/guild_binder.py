import discord
from discord import guild
from discord.ext import commands
from discord import app_commands

from utilities.db_manager.db_manager import GUILD_IDS, get_enabled_modules_for_guild

from utilities.sync_engine.custom_group import REGISTERED_GROUPS

async def rebuild_commands_for_guild(bot: commands.Bot, guild_id: int):
    tree: app_commands.CommandTree = bot.tree
    guild_obj = discord.Object(id=guild_id)

    enabled_modules = await get_enabled_modules_for_guild(guild_id)

    commands_for_guild: list[app_commands.Command | app_commands.Group] = []


    # handleing normal commands

    for command in tree.walk_commands():
        # skip groups
        if isinstance(command, app_commands.Group):
            continue

        callback = getattr(command, "callback", None)
        if callback is None:
            continue

        module_name = getattr(callback, "__module_name__", None)
        
        if module_name and module_name not in enabled_modules:
            continue

        commands_for_guild.append(command)

    # handleing groups
    for group in REGISTERED_GROUPS:
        allowed_subcommands: list[app_commands.Command] = []

        for sub in group.commands:
            callback = getattr(sub, "callback", None)
            if callback is None:
                continue

            module_name = getattr(callback, "__module_name__", None)

            if module_name and module_name not in enabled_modules:
                continue

            allowed_subcommands.append(group)

    #clearing all guild specific commands for that guild
    tree.clear_commands(guild=guild_obj)

    #reading commands
    for cmd in commands_for_guild:
        tree.add_command(cmd, guild=guild_obj)

    name = [cmd.qualified_name for cmd in commands_for_guild]
    print(f"[SYNC ENGINE] Rebuilt commands for guild {guild_id}: {len(commands_for_guild)} commands -> {name}")