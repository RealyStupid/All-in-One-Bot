from utilities.config.cog_deps import *

from utilities.sync_engine.guild_binder import sync_guild
import utilities.db_manager.db_manager as db
class SyncManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx, sync_type: str = None):
        """Syncs the bot's commands with Discord. (Owner only)"""
        guild_id: list[int] = db.GUILD_IDS

        await ctx.send("syncing commands")

        total = 0
        for guilds in guild_id:
            synced = await sync_guild(self.bot, guilds)
            total += len(synced)

        await ctx.send(f"synced {total} commands across {len(guild_id)} guilds")
        
async def setup(bot):
    await bot.add_cog(SyncManager(bot))
        
