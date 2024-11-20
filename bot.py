import discord

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()
discord_bot_token = "token here"
channel_id = '1308389878630711309'

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = client.get_channel(int(channel_id))
        await channel.send("안녕")

async def on_message(self, message):
    if message.author == client.user:

        print(f'Message from me {message.author}: {message.content}')
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello!')
        print(f'Message from {message.author}: {message.content}')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_bot_token)