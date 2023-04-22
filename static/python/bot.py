import discord
from discord import app_commands
from discord.ext import commands
from polly_req import PollySession
import subprocess
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="ssml", description="Test your TTS! You can use plain text, SSML, Bikubot shorthand, or a mix of all of them!")
async def ssml(interaction: discord.Interaction, text: str):
    result = subprocess.run(['node', '../js/biku_interface.mjs', text], stdout=subprocess.PIPE).stdout.decode('utf-8')
    p = PollySession(result)
    filePath = p.generateMP3File()
    await interaction.response.send_message(text, file=discord.File(filePath))
    p.deleteMP3File(filePath)

bot.run(os.environ["SSML_BOT_KEY"])