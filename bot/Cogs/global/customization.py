from utilities.config.cog_deps import *

import utilities.db_manager.db_manager as db

class Customization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    customization = app_commands.Group(name="customization", description="Commands for customizing the bot's appearance.")

    @customization.command(name="prefix", description="Set the bot's prefix wanting to be used")
    async def set_prefix(self, interaction: discord.Interaction, prefix: str):
        await db.set_prefix(interaction.guild_id, prefix)
        await interaction.response.send_message(f"Prefix set to: {prefix}")

    @customization.command(name="nickname", description="Set the bot's nickname in this server")
    async def set_nickname(self, interaction: discord.Interaction, nickname: str):
        try:
            await interaction.guild.me.edit(nick=nickname)
            await interaction.response.send_message(f"Nickname set to: {nickname}")
        except Exception as e:
            await interaction.response.send_message(f"Failed to set nickname: {e}")

async def setup(bot):
    await bot.add_cog(Customization(bot))
    
