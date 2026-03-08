import discord
from discord.ext import commands


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commands", aliases=["cmds", "helpme"])
    async def list_prefix_commands(self, ctx: commands.Context):
        """
        Shows all prefix commands loaded in the bot.
        """
        prefix = ctx.prefix  # dynamic prefix support
        commands_list = []

        for cmd in self.bot.commands:
            # Skip hidden commands
            if cmd.hidden:
                continue

            # Format command with signature
            signature = f"{prefix}{cmd.name}"
            if cmd.signature:
                signature += f" {cmd.signature}"

            commands_list.append(
                f"**{signature}** — {cmd.help or 'No description'}"
            )

        # Sort alphabetically
        commands_list.sort()

        # Build embed
        embed = discord.Embed(
            title="📜 Prefix Commands",
            description="\n".join(commands_list) if commands_list else "No commands found.",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandList(bot))