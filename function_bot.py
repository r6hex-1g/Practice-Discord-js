#!/usr/bin/env python
import discord
from discord.ext import commands
from discord import ui
from discord.interactions import Interaction
import os
import sys
import time

bot = commands.Bot(command_prefix='|',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("봇 실행")
    synced = await bot.tree.sync()
    print(f"Slash Command {len(synced)}")

@bot.tree.command(name="restart")
async def restart(interaction: discord.Interaction):
        await interaction.response.send_message("봇이 리부팅됩니다...")

        time.sleep(2)

        os.execv(sys.executable, ['python'] + sys.argv)

class MyModal(ui.Modal, title = "test 제목 필드 입니다."):
    name = ui.TextInput(label="경고 대상자", placeholder="경고 대상자", style=discord.TextStyle.short)
    name2 = ui.TextInput(label="경고 횟수", placeholder="경고 횟수", style=discord.TextStyle.long)
    name3 = ui.TextInput(label="경고 사유", placeholder="경고 사유", style=discord.TextStyle.short)
    name4 = ui.TextInput(label="경고 집행자", placeholder="경고 집행자", style=discord.TextStyle.short)


    async def on_submit(self, interaction: discord.Interaction):
        message = (
            f"경고 대상자: {self.name}\n"
            f"경고 횟수: {self.name2}\n"
            f"경고 사유: {self.name3}\n"
            f"경고 집행자: {self.name4}"
        )
        await interaction.response.send_message(message)

@bot.tree.command(name="warning")
async def warning(interaction: discord.Interaction):
    message = "이것은 경고 메시지입니다."
    await interaction.response.send_message(message)


class SelectMenu(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="test1",description="test1 설명",emoji="📊"),
                discord.SelectOption(label="test2",description="test2 설명",emoji="📉"),
                discord.SelectOption(label="test3",description="test3 설명",emoji="📈"),]
        super().__init__(placeholder = "Select 메뉴 창 입니다.", options = options, min_values=1, max_values=3)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"{self.values}")

class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectMenu())

@bot.tree.command(name="select")
async def select(interaction: discord.Interaction):
    await interaction.response.send_message(content="여기는 1번content", view=Select())



bot.run('봇토큰')