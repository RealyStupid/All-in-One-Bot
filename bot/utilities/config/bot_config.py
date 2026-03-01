import discord
import os
from dotenv import load_dotenv

# Getting the bot token here
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Application ID
APPLICATION_ID = 1476275066210746558

# Prefix command
COMMAND_PREFIX = "!"

# Setting intents for the bot
INTENTS = discord.Intents.default()
INTENTS.message_content = True