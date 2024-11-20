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

NOTIFICATION_CHANNEL_ID = 1308743159768940544
AUTHORIZED_USERS = [1175816769529716837, 738298583895375974]

@bot.event
async def on_ready():
    print(f"{bot.user}가 실행되었습니다.")
    try:
        synced = await bot.tree.sync()
        print(f"슬래시 명령어 {len(synced)}개 동기화 완료")

        channel = bot.get_channel(1308743159768940544)
        if channel:
            await channel.send("✅ 봇이 성공적으로 리부팅되었습니다!")
        else:
            print("알림 채널을 찾을 수 없습니다.")
    except Exception as e:
        print(f"슬래시 명령어 동기화 오류: {e}")

@bot.tree.command(name="restart")
async def restart(interaction: discord.Interaction):
        if interaction.user.id in AUTHORIZED_USERS:

            await interaction.response.send_message("리부팅을 시작합니다. 봇이 곧 다시 온라인 상태가 됩니다!")

        channel = bot.get_channel(738298583895375974)

        if channel:
            log_message = (
                f"⚠️ **리부팅 명령 실행**\n"
                f"- 실행자: {interaction.user.mention}\n"
                f"- 실행자 ID: `{interaction.user.id}`\n"
                f"- 실행 시간: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
                f"- 상태: 리부팅을 시작합니다..."
            )

            await channel.send(log_message)
            await bot.close()
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            await interaction.response.send_message("이 명령어를 사용할 권한이 없습니다.", ephemeral=True)

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

@bot.tree.command(name="문의")
async def inquiry(interaction: discord.Interaction):

    class InquiryModal(ui.Modal, title="문의 내용"):
        question = ui.TextInput(label="문의 내용", placeholder="문의 내용을 입력해주세요", style=discord.TextStyle.long)

        async def on_submit(self, interaction: discord.Interaction):
           inquiry_content = self.question.value
           current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

           channel = bot.get_channel(1308786597986045962)
           
           if channel:
               embed = discord.Embed(
                   title="📩 새 문의가 도착했습니다!",
                   description="사용자가 새로운 문의를 남겼습니다. 아래 내용을 확인해주세요.",
                   color=discord.Color.blue()
               )
               embed.add_field(name="문의 내용", value=inquiry_content, inline=False)
               embed.add_field(name="문의자", value=interaction.user.mention, inline=True)
               embed.add_field(name="문의 시간", value=current_time, inline=True)

               await channel.send(embed=embed)
               await interaction.response.send_message("문의가 성공적으로 전송되었습니다. 관리자가 곧 답변할 것입니다!", ephemeral=True)
            else:
               await interaction.response.send_message("문의 전송 중 오류가 발생했습니다.", ephemeral=True)

class ReportSelectMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="경고 시스템", description="경고 대상자를 등록", emoji="⚠️"),
            discord.SelectOption(label="문의 내용", description="관리자에게 문의", emoji="📩")
        ]
        super().__init__(placeholder="신고/문의 유형을 선택하세요.", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "경고 시스템":
            modal = MyModal()
            await interaction.response.send_modal(modal)
        elif self.values[0] == "문의 내용":
            modal = InquiryModal()
            await interaction.response.send_modal(modal)

class ReportView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ReportSelectMenu())

@bot.tree.command(name="report")
async def report(interaction: discord.Interaction):
    await interaction.response.send_message("경고 또는 문의를 선택해주세요.", view=ReportView())

bot.run('봇 토큰')