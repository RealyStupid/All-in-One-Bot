from utilities import *

class GuildManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -----------------------------
    # LISTENER: When bot joins a guild
    # -----------------------------
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await db.register_guild(guild.id)
        print(f"Registered guild {guild.id} in the database")

    # -----------------------------
    # OWNER-ONLY: Register guild manually
    # -----------------------------
    @commands.command(
        name="register",
        description="Registers the guild in the database. (Owner only)"
    )
    @commands.is_owner()
    async def register(self, ctx: commands.Context):
        await db.register_guild(ctx.guild.id)
        await ctx.send("Guild registered in the database!")

    # -----------------------------
    # OWNER-ONLY: Unregister guild manually
    # -----------------------------
    @commands.command(
        name="unregister",
        description="Unregisters the guild from the database. (Owner only)"
    )
    @commands.is_owner()
    async def unregister(self, ctx: commands.Context):
        await db.unregister_guild(ctx.guild.id)
        await ctx.send("Guild unregistered from the database!")

    # -----------------------------
    # OWNER-ONLY: List all registered guilds
    # -----------------------------
    @commands.command(
        name="guilds",
        description="Lists all registered guilds in the database. (Owner only)"
    )
    @commands.is_owner()
    async def guilds(self, ctx: commands.Context):
        guild_ids: list[int] = db.GUILD_IDS

        if not guild_ids:
            await ctx.send("No guilds registered in the database.")
            return

        message = "Registered guilds:\n" + "\n".join(f"- {gid}" for gid in guild_ids)
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(GuildManager(bot))