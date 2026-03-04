'''
This file contains the main entry point for the bot.
It defines the Client class, which inherits from commands.Bot, and sets up the bot's configuration and event handlers.
The bot initializes the database manager and prints a message when it is ready.
'''

import discord
from discord.ext import commands

import os

from utilities.config.bot_config import INTENTS, APPLICATION_ID, COMMAND_PREFIX, BOT_TOKEN
import utilities.db_manager.db_manager as db


# helper function
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

        await db.init_data(path="utilities\\db_manager\\data\\guild_cache.db", new_instance=True)

        await self.load_all_cogs("Cogs")

    async def load_all_cogs(self, directory):
        base = directory.replace("\\", "/")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    full_path = os.path.join(root, file).replace("\\", "/")

                    relative = full_path[len(base):].lstrip("/")

                    module = f"Cogs.{relative[:-3].replace('/', '.')}"

                    await self.load_extension(module)
                    print(f"Loaded cog: {module}")

    async def on_ready(self):
        print("----------------------------------------------------------------------------------------\n"
              f"[BOT STARTED] {self.user} (user id: {self.user.id} | application id: {APPLICATION_ID})\n"
              "----------------------------------------------------------------------------------------")

bot = Client()

# temporary syncing system, will be replaced sync engine in the future
@bot.command(name="sync", description="Syncs the bot's commands with Discord. (Admin only)")
@commands.has_permissions(administrator=True)
async def sync(ctx, type: str = None):
    
    if type == "global":
        try:
            await bot.tree.sync()
            print("Successfully synced global commands")
        except Exception as e:
            print(f"Failed to sync global commands: {e}")
    
    elif type == None or type == "guilds":
        for guild_id in db.GUILD_IDS:
            total = 0
            try:
                synced = await bot.tree.sync(guild=discord.Object(id=guild_id))
                total += len(synced)
            except Exception as e:
                print(f"Failed to sync commands for guild {guild_id}: {e}")

    await ctx.send(f"Synced {total} commands across {len(db.GUILD_IDS)} guilds!")

@bot.command(name="register", description="Registers the current guild in the database. (Admin only)")
@commands.has_permissions(administrator=True)
async def register(ctx):
    await db.register_guild(ctx.guild.id)
    await ctx.send("Guild registered in the database!")

@bot.event
async def on_guild_join(guild):
    await db.register_guild(guild.id)
    print(f"Registered guild {guild.id} in the database")

    await sync(type="guilds")

bot.run(BOT_TOKEN)