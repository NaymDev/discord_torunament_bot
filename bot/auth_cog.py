from typing import Any, Optional, Union
import discord
from discord.colour import Colour
from discord.ext import commands
from discord.types.embed import EmbedType
from discord.utils import MISSING
import traceback

from API import auth
from bot import storage

class AuthCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    @commands.command(name="auth")
    async def auth(self, ctx: commands.Context):
        if ctx.channel == self.bot.CHANNEL["login"]:
            await ctx.send(content="You will be authenticated soon...", ephemeral=True)
            await ctx.send_modal(AuthModal())
        else:
            await ctx.send(content="This command can only be used in the `login` channel.", ephemeral=True)
        await ctx.message.delete()

    @commands.command(name="auth_server")
    async def auth_server(self, ctx: commands.Context):
        if ctx.channel == self.bot.CHANNEL["login"]:
            await ctx.send(content="IP: 1.1.1.1:1022\nMinecraft version: 1.20.1 java", ephemeral=True)
            await ctx.send(content="[INFO] You will have to be on the server to authenticate!", ephemeral=True)
        else:
            await ctx.send(content="This command can only be used in the `login` channel.", ephemeral=True)
        await ctx.message.delete()


class AuthModal(discord.ui.Modal):
    igname = discord.ui.TextInput(label="Name: ", style= discord.TextStyle.short, required=True, min_length=3, max_length=40)
    code = discord.ui.TextInput(label="Code: ", style= discord.TextStyle.short, required=True, min_length=6, max_length=6)
    info = discord.ui.TextInput(label="Info", max_length=500,style=discord.TextStyle.long, required=False, placeholder="Join auth.mc-oauth.com(1.8.x-1.19.x) to recive the code.")
    
    def __init__(self, user, log) -> None:
        super().__init__(title="Authentication: get Auth. code")
        self.user: discord.User = user
        self.log_ch = log

    async def on_submit(self, interaction: discord.Interaction):
        if storage.USER[interaction.user.id].is_timeout():
            await interaction.response.send_message(f"You have to wait {storage.USER[interaction.user.id].remaining_time_string()} until you can try again." ,ephemeral=True)
        if storage.USER[interaction.user.id].igname != "": 
            await interaction.response.send_message("You are already authenticated with this account!", ephemeral=True)
            return
        res = auth.AuthenticateCode(self.code.value, self.igname.value)
        if res:
            await interaction.response.send_message("We authenticated your minecraft account succesfuly!" ,ephemeral=True)
            await self.log(1, f"{interaction.user.name} authenticated succesfuly with '{self.igname.value}'!")
            storage.USER[interaction.user.id].igname = self.igname.value #Store igname
            storage.USER[interaction.user.id].auth_timeout(60) #Timeout user
            storage.save_data("storage.consumer") #Save new data
        elif res == None:
            await self.log(1, f"{interaction.user.name} tried authenticating with '{self.igname.value}'!")
            await interaction.response.send_message("We could't authenticate you.If this keeps happening please ask a supporter!\nYou entered the wrong username/password.", ephemeral=True)
            storage.USER[interaction.user.id].auth_timeout()
            
    
    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
    
    async def log(self, level, message):
        if(level==1):
            await self.log_ch.send("**[AUTH]** "+message)

async def setup(bot):
    await bot.add_cog(AuthCog(bot))