#!/usr/bin/env python
import discord
from discord.ext import commands
from discord import ui
from discord.interactions import Interaction
import os
import sys
import asyncio
from datetime import datetime

bot = commands.Bot(command_prefix='|',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user}가 실행되었습니다.")
    try:
        synced = await bot.tree.sync()
        print(f"슬래시 명령어 {len(synced)}개 동기화 완료")
    except Exception as e:
        print(f"슬래시 명령어 동기화 오류: {e}")

@bot.tree.command(name="restart")
async def restart(interaction: discord.Interaction):
        await interaction.response.send_message("봇이 리부팅됩니다...")
        await asyncio.sleep(2)
        os.execv(sys.executable, ['python'] + sys.argv)

class MyModal(ui.Modal, title = "경고 시스템"):
    name = ui.TextInput(label="경고 대상자", placeholder="경고 대상자", style=discord.TextStyle.short)
    name2 = ui.TextInput(label="경고 횟수", placeholder="경고 횟수", style=discord.TextStyle.long)
    name3 = ui.TextInput(label="경고 사유", placeholder="경고 사유", style=discord.TextStyle.short)
    name4 = ui.TextInput(label="경고 집행자", placeholder="경고 집행자", style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

        embed = discord.Embed(
            title="⚠️ 경고자가 생겼어요!",
            description="아래의 경고자 분은 자신의 경고를 확인하시고 꼭 이의가 생긴다면 문의해주세요!",
            color=discord.Color.yellow()
        )
        embed.add_field(name="경고 대상자", value=self.name.value, inline=False)
        embed.add_field(name="경고 횟수", value=self.name2.value, inline=True)
        embed.add_field(name="경고 사유", value=self.name3.value, inline=False)
        embed.add_field(name="경고 집행자", value=self.name4.value, inline=True)
        embed.set_footer(text=f"경고 발행 시간: {current_time}")

        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="warning")
async def warning(interaction: discord.Interaction):
    modal = MyModal()
    await interaction.response.send_modal(modal)


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



bot.run('봇 토큰')