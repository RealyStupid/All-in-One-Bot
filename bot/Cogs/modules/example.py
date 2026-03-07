from utilities.config.cog_deps import *

class ExampleCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# this is a command is set to the "test" module.
	@app_commands.command(name='test_command', description='this is an example of a command with only modules set')
	@module("test")
	async def testcommand(self, interaction: discord.Interaction):
		await interaction.response.send_message("this is an example of a command with only modules set")

	group = create_group(name="super_test", description="this is a group made by the custom group")

	@group.command(name="testssss", description="this command is built with a custom group")
	@module("test")
	async def anothertest(self, interaction: discord.Interaction):
		await interaction.response.send_message("this command is made by the custom group")


async def setup(bot):
	await bot.add_cog(ExampleCog(bot))