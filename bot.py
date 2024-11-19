import discord
import os

import discord

discord_bot_token = os.enciron.get('bot token here')
channel_id = '1308415682895151134'

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


intents = discord.lntents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_bot_token)