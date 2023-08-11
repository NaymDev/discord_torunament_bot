from typing import Any, Optional, Union
import discord
from discord.colour import Colour
from discord.ext import commands
from discord.types.embed import EmbedType
from discord.utils import MISSING
import traceback

from API import auth
from bot import storage

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    


async def setup(bot):
    await bot.add_cog(AdminCog(bot))