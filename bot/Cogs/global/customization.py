from utilities import *


# ---------------------------------------------------------
# GLOBAL GROUP DEFINITION
# ---------------------------------------------------------
# Mark this group as GLOBAL by passing module=None
customization = Group(
    "customization",
    "Commands for customizing the bot's appearance."
)


# ---------------------------------------------------------
# GLOBAL SLASH COMMANDS
# ---------------------------------------------------------

@customization.command("prefix", "Set the bot's prefix for this server")
@owner_only()
@module(None)
async def set_prefix(interaction: discord.Interaction, prefix: str):
    await db.set_prefix(interaction.guild_id, prefix)
    await interaction.response.send_message(f"Prefix set to: {prefix}")


@customization.command("nickname", "Set the bot's nickname in this server")
@owner_only()
@module(None)
async def set_nickname(interaction: discord.Interaction, nickname: str):
    try:
        await interaction.guild.me.edit(nick=nickname)
        await interaction.response.send_message(f"Nickname set to: {nickname}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to set nickname: {e}")


# ---------------------------------------------------------
# COG (PREFIX COMMANDS OR LISTENERS ONLY)
# ---------------------------------------------------------
class Customization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Customization(bot))