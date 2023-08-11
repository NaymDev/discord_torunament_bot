from typing import Optional
import discord
from discord.ext import commands

import logging

from discord.message import Message

from bot import auth_cog
from API import auth
from bot import storage

import datetime, json

class TournamentBot(commands.Bot):
    def __init__(
        self,
        *args,
        logger: logging.Logger,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.CHANNEL = CHANNEL = {
            "login":1138411768658530374,
            "general":1138411657698230344,
            "log":1138417097676959774
        }

    
    async def on_ready(self):
        storage.read_data("storage.consumer")
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        for key, value in self.CHANNEL.items():
            self.CHANNEL[key] = self.guilds[0].get_channel(value)
        print("Started")
        await self.tree.sync()

        class MyView(discord.ui.View):
            def __init__(self, *, timeout: float | None = 180, log):
                super().__init__(timeout=timeout)
                self.log = log

            @discord.ui.button(label="Auth.", style=discord.ButtonStyle.primary)
            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(auth_cog.AuthModal(user=interaction.user, log=self.log))

        view = MyView(log=self.CHANNEL["log"])
        await self.CHANNEL["login"].send(content="Authenticate your minecraft account to participate on the tournament.", view=view)
    
    async def on_member_join(self, member):
        storage.USER[member.id] = storage.User(member.name, "")
        storage.save_data("storage.consumer")
        guild: discord.Guild = member.guild
        if self.CHANNEL["general"] is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!\nYou can use `?auth` to verify your minecraft account to participate at the tournament.Do `?auth_server` to get more information about the server!'
            await self.CHANNEL["general"].send(to_send)
    
    async def on_message(self, message: Message) -> None:#
        if message.author == self.user:
            return
        if message.channel == self.CHANNEL["login"] and not message.content.startswith("?"):
            await message.delete()
        else:
            await self.process_commands(message)
        if message.content.startswith("?"):
            await message.delete()
    
    async def log(self, level, message):
        if(level==1):
            await self.CHANNEL["log"].send("**[AUTH]** "+message)
        elif(level==2):
            await self.CHANNEL["log"].send("**[TEAM]** "+message)