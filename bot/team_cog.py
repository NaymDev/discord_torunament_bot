import discord
from discord.colour import Colour
from discord.ext import commands
from discord.types.embed import EmbedType
from discord.utils import MISSING

import traceback
from typing import Any, Optional, Union

from API import auth
from bot import storage

class TeamCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
    
    async def on_ready(self):
        self.bot.tree.sync()

    @discord.app_commands.command(name="team")
    @discord.app_commands.describe(user_a="First user", user_b="Second user", color="Team color: #<hex>")
    async def team(self, ctx: discord.Interaction, name: str, user_a: discord.User, user_b: discord.User, color: Optional[str]):
        if storage.USER[ctx.user.id].igname == "":
            await ctx.response.send_message("You have to be verified to create a team!", ephemeral=True)
            return
        if storage.USER[user_a.id].igname == '' or storage.USER[user_b.id].igname == '':
            await ctx.response.send_message("One or both other users aren't verified!", ephemeral=True)
            return
        await ctx.response.send_message(f"{user_a.name} and {user_b.name} recived a invite!")
        class MyView(discord.ui.View):
            def __init__(self, *, timeout: float | None = 180, log, team):
                super().__init__(timeout=timeout)
                self.log = log
                self.team = team

            @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                team: discord.Role = await interaction.guild.get_role(self.team)
                interaction.user.roles.append(team)
                await interaction.response.send_message(f"You are now in the team({team.name})!")
                for user in storage.TEAMS[self.team]:
                    commands.Bot(interaction.message.author).get_user(user).send(f"{interaction.user.name} joined the Team!")
                storage.TEAMS[self.team].append(interaction.user.id)
                storage.save_data("storage.consumer")

        await ctx.guild.create_role(name=name)
        team: discord.Role = discord.utils.get(ctx.guild.roles, name=name)
        team.hoist = True
        if color:
            try:
                await team.edit(color=discord.Color.from_str(color))
            except:
                ctx.response.send_message(f"Invalid color {color}.Please use #<hex>!")
                await team.edit(color=discord.Color.red)
        else:
            await team.edit(color=discord.Color.blue)

        storage.TEAMS[team.id] = [ctx.user.id]
        storage.save_data("storage.consumer")
        ctx.user.roles.append(team)
        view = MyView(log=self.bot.CHANNEL["log"], team=team.id)
        await user_a.send(content=f"{ctx.user.name} invited you to join his team.", view=view)
        await user_b.send(content=f"{ctx.user.name} invited you to join his team.", view=view)

async def setup(bot):
    await bot.add_cog(TeamCog(bot))