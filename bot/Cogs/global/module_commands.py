from utilities.config.cog_deps import *
from utilities.sync_engine.module_enum import ModuleEnum
import utilities.db_manager.db_manager as db

class ModuleControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    module = app_commands.Group(name="module", description="Commands for enabling and disabling modules")

    # auto fills the module name based on the enum,
    # and only shows modules that are relevant to the command (enabled for disable, disabled for enable)
    async def autocomplete_enable_modules(
        self,
        interaction: discord.Interaction,
        current: str
    ):
        """Autocomplete for /module enable — only show disabled modules"""
        guild_id = interaction.guild_id
        enabled = await db.get_enabled_modules_for_guild(guild_id)

        return [
            app_commands.Choice(name=m.value, value=m.value)
            for m in ModuleEnum
            if m.value not in enabled and current.lower() in m.value.lower()
        ]

    async def autocomplete_disable_modules(
        self,
        interaction: discord.Interaction,
        current: str
    ):
        """Autocomplete for /module disable — only show enabled modules"""
        guild_id = interaction.guild_id
        enabled = await db.get_enabled_modules_for_guild(guild_id)

        return [
            app_commands.Choice(name=m.value, value=m.value)
            for m in ModuleEnum
            if m.value in enabled and current.lower() in m.value.lower()
        ]

    # The commands for enabling, disabling, and listing modules
    @module.command(name="list", description="List all modules")
    @commands.has_permissions(administrator=True)
    async def list_modules(self, interaction: discord.Interaction):
        all_modules = [m.value for m in ModuleEnum]

        embed = discord.Embed(
            title="📦 All Modules",
            description="\n".join(f"- `{m}`" for m in all_modules),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @module.command(name="enabled", description="List enabled modules")
    @commands.has_permissions(administrator=True)
    async def enabled_modules(self, interaction: discord.Interaction):
        guild_id = interaction.guild_id
        enabled = await db.get_enabled_modules_for_guild(guild_id)

        if not enabled:
            await interaction.response.send_message("No modules are currently enabled.")
        else:
            embed = discord.Embed(
                title="✅ Enabled Modules",
                description="\n".join(f"- `{m}`" for m in enabled),
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)

    @module.command(name="enable", description="Enable a module")
    @commands.has_permissions(administrator=True)
    @app_commands.autocomplete(module_name=autocomplete_enable_modules)
    async def enable_module(self, interaction: discord.Interaction, module_name: str):
        guild_id = interaction.guild_id
        await db.set_module_enabled(guild_id, module_name, True)
        await interaction.response.send_message(f"Module `{module_name}` has been enabled.")

    @module.command(name="disable", description="Disable a module")
    @commands.has_permissions(administrator=True)
    @app_commands.autocomplete(module_name=autocomplete_disable_modules)
    async def disable_module(self, interaction: discord.Interaction, module_name: str):
        guild_id = interaction.guild_id
        await db.set_module_enabled(guild_id, module_name, False)
        await interaction.response.send_message(f"Module `{module_name}` has been disabled.")

async def setup(bot):
    await bot.add_cog(ModuleControl(bot))