# bot.py
import os
import logging
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)


bot = commands.Bot(command_prefix=".", intents=intents)

async def main():
    #await bot.load_extension("bot.auth_cog")
    await bot.start(TOKEN)

bot.run(TOKEN)

#https://minotar.net/bust/user/100.png