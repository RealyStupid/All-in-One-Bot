import discord
from discord.ext import commands

from utilities.config.bot_config import INTENTS, APPLICATION_ID, COMMAND_PREFIX, BOT_TOKEN
from utilities.db_manager.db_manager import init_data

class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=INTENTS,
            application_id=APPLICATION_ID
        )

    async def setup_hook(self):
        print("[SETTING UP BOT] The bot starting setting up everything before logging in")

        await init_data("utilities\\db_manager\\data\\guild_cache.db", new_instance=True)

    async def on_ready(self):
        print("----------------------------------------------------------------------------------------\n"
              f"[BOT STARTED] {self.user} (user id: {self.user.id} | application id: {APPLICATION_ID})\n"
              "----------------------------------------------------------------------------------------")

bot = Client()

bot.run(BOT_TOKEN)