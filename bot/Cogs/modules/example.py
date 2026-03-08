from utilities import *

@slash.command("command_name", "a basic command that just sends a message")
@module("test")
async def command_name(interaction: discord.Interaction):
    await interaction.response.send_message("some message")

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Example(bot))