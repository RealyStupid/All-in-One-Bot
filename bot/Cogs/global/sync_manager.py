from discord.ext import commands
import discord

from utilities.sync_engine.guild_binder import sync_guild, sync_global
import utilities.db_manager.db_manager as db

class SyncManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="sync",
        description="Syncs the bot's commands with Discord. (Owner only)"
    )
    @commands.is_owner()
    async def sync(self, ctx, sync_type: str = None):
        """
        Sync slash commands using the custom sync engine.

        Usage:
        !sync            → sync all guilds
        !sync guild      → sync only this guild
        !sync global     → sync global commands
        !sync clear      → clear + resync this guild
        """

        # -----------------------------
        # SYNC ONLY THIS GUILD
        # -----------------------------
        if sync_type == "global":
            await ctx.send("🌍 Syncing **global** commands...")

            synced = await sync_global(self.bot)

            return await ctx.send(
                f"🌐 Synced **{len(synced)}** global commands."
            )

        # -----------------------------
        # CLEAR + RESYNC THIS GUILD
        # -----------------------------
        if sync_type == "clear":
            await ctx.send(f"🧹 Clearing commands for **{ctx.guild.name}**...")

            # Clear commands for this guild
            self.bot.tree.clear_commands(guild=ctx.guild)

            # Resync
            synced = await self.bot.tree.sync(guild=ctx.guild)

            return await ctx.send(
                f"♻️ Cleared and resynced **{len(synced)}** commands for **{ctx.guild.name}**."
            )

        # -----------------------------
        # SYNC GLOBAL COMMANDS
        # -----------------------------
        if sync_type == "global":
            await ctx.send("🌍 Syncing **global** commands...")

            synced = await self.bot.tree.sync()  # global sync

            return await ctx.send(
                f"🌐 Synced **{len(synced)}** global commands."
            )

        # -----------------------------
        # DEFAULT: SYNC ALL GUILDS
        # -----------------------------
        guild_ids: list[int] = db.GUILD_IDS

        await ctx.send("🔄 Syncing commands across all guilds...")

        total = 0
        for guild_id in guild_ids:
            synced = await sync_guild(self.bot, guild_id)
            total += len(synced)

        await ctx.send(
            f"✅ Synced **{total}** commands across **{len(guild_ids)}** guilds."
        )


async def setup(bot):
    await bot.add_cog(SyncManager(bot))