from utilities.config.cog_deps import *
import utilities.db_manager.db_manager as db
class GuildManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(guild):
        await db.register_guild(guild.id)
        print(f"Registered guild {guild.id} in the database")


    @commands.command(name="register", description="Registers the guild in the database. (Owner of bot only)")
    @commands.is_owner()
    async def register(self, ctx):
        await db.register_guild(ctx.guild.id)
        await ctx.send("Guild registered in the database!")

    @commands.command(name="unregister", description="Unregisters the guild from the database. (Owner of bot only)")
    @commands.is_owner()
    async def unregister(self, ctx):
        await db.unregister_guild(ctx.guild.id)
        await ctx.send("Guild unregistered from the database!")

    @commands.command(name="guilds", description="Lists all registered guilds in the database. (Owner of bot only)")
    @commands.is_owner()
    async def guilds(self, ctx):
        guild_ids: list[int] = db.GUILD_IDS

        message_string = "Registered guilds in the database:\n"

        if not guild_ids:
            message_string += "No guilds registered in the database."
        else:
            message_string += "\n".join([f"- {guild_id}" for guild_id in guild_ids])

        await ctx.send(message_string)

async def setup(bot):
    await bot.add_cog(GuildManager(bot))