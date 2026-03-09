from pickle import TRUE
from utilities import *
from utilities.custom_command_api.module_enum import ModuleEnum

from utilities.sync_engine.guild_binder import sync_guild

# ---------------------------------------------------------
# GLOBAL GROUP DEFINITION
# ---------------------------------------------------------
module_group = Group(
    "module",
    "Commands for enabling and disabling modules"
)

# ---------------------------------------------------------
# AUTOCOMPLETE FUNCTIONS
# ---------------------------------------------------------
async def autocomplete_enable_modules(interaction: discord.Interaction, current: str):
    """Autocomplete for /module enable — only show disabled modules."""
    guild_id = interaction.guild_id
    enabled = await db.get_enabled_modules_for_guild(guild_id)

    return [
        discord.app_commands.Choice(name=m.value, value=m.value)
        for m in ModuleEnum
        if m.value not in enabled and current.lower() in m.value.lower()
    ]


async def autocomplete_disable_modules(interaction: discord.Interaction, current: str):
    """Autocomplete for /module disable — only show enabled modules."""
    guild_id = interaction.guild_id
    enabled = await db.get_enabled_modules_for_guild(guild_id)

    return [
        discord.app_commands.Choice(name=m.value, value=m.value)
        for m in ModuleEnum
        if m.value in enabled and current.lower() in m.value.lower()
    ]

# ---------------------------------------------------------
# GLOBAL SLASH COMMANDS
# ---------------------------------------------------------
@module_group.command("list", "List all modules")
@owner_only(allow_guild_owner=True)
@module(None)
async def list_modules(interaction: discord.Interaction):
    all_modules = [m.value for m in ModuleEnum]

    embed = discord.Embed(
        title="📦 All Modules",
        description="\n".join(f"- `{m}`" for m in all_modules),
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(embed=embed)


@module_group.command("enabled", "List enabled modules")
@owner_only(allow_guild_owner=True)
@module(None)
async def enabled_modules(interaction: discord.Interaction):
    guild_id = interaction.guild_id
    enabled = await db.get_enabled_modules_for_guild(guild_id)

    if not enabled:
        await interaction.response.send_message("No modules are currently enabled.")
        return

    embed = discord.Embed(
        title="✅ Enabled Modules",
        description="\n".join(f"- `{m}`" for m in enabled),
        color=discord.Color.green()
    )

    await interaction.response.send_message(embed=embed)


@module_group.command("enable", "Enable a module")
@owner_only(allow_guild_owner=True)
@autocomplete(module_name=autocomplete_enable_modules)
@module(None)
async def enable_module(interaction: discord.Interaction, module_name: str):
    guild_id = interaction.guild_id

    # 1. Acknowledge immediately (prevents timeout)
    await interaction.response.defer(ephemeral=True)

    # 2. Update DB
    await db.set_module_enabled(guild_id, module_name, True)

    # 3. Sync commands
    await sync_guild(interaction.client, guild_id)

    # 4. Send final message
    await interaction.followup.send(
        f"Module `{module_name}` has been enabled and commands synced."
    )


@module_group.command("disable", "Disable a module")
@owner_only(allow_guild_owner=True)
@autocomplete(module_name=autocomplete_disable_modules)
@module(None)
async def disable_module(interaction: discord.Interaction, module_name: str):
    guild_id = interaction.guild_id

    # 1. Acknowledge immediately
    await interaction.response.defer(ephemeral=True)

    # 2. Update DB
    await db.set_module_enabled(guild_id, module_name, False)

    # 3. Sync commands
    await sync_guild(interaction.client, guild_id)

    # 4. Send final message
    await interaction.followup.send(
        f"Module `{module_name}` has been disabled and commands synced."
    )

# ---------------------------------------------------------
# COG (PREFIX COMMANDS OR LISTENERS ONLY)
# ---------------------------------------------------------
class ModuleControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ModuleControl(bot))