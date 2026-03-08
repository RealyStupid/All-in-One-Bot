import discord
from discord.ext import commands
import os

from utilities.config.bot_config import INTENTS, APPLICATION_ID, COMMAND_PREFIX, BOT_TOKEN
import utilities.db_manager.db_manager as db

from utilities.sync_engine.execution_manager import register_global_commands


async def dynamic_prefix(bot, message):
    if not message.guild:
        return "!"
    return await db.get_prefix(message.guild.id)


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=dynamic_prefix,
            intents=INTENTS,
            application_id=APPLICATION_ID
        )

    async def setup_hook(self):
        print("[SETTING UP BOT] The bot starting setting up everything before logging in")

        await db.init_data(path="utilities\\db_manager\\data\\guild_cache.db", new_instance=False)

        # 1) Load all cogs (this populates the custom command registry)
        await self.load_all_cogs("Cogs")

        # 2) Register global commands for execution (from the now-populated registry)
        await register_global_commands(self)

        # Note: actual syncing is still done manually via !sync / !sync global

    async def load_all_cogs(self, directory):
        base = directory.replace("\\", "/")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    full_path = os.path.join(root, file).replace("\\", "/")
                    relative = full_path[len(base):].lstrip("/")
                    module = f"Cogs.{relative[:-3].replace('/', '.')}"
                    await self.load_extension(module)
                    print(f"[COG LOADER] Loaded cog {module}")

    async def on_ready(self):
        print("----------------------------------------------------------------------------------------")
        print(f"[BOT STARTED] {self.user} (user id: {self.user.id} | application id: {APPLICATION_ID})")
        print("----------------------------------------------------------------------------------------")


bot = Client()
bot.run(BOT_TOKEN)