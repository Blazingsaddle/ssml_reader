import discord
from discord import app_commands
from discord.ext import commands
from polly_req import PollySession
import subprocess
import os

class ButtonView(discord.ui.View):
    def __init__(self, text, interaction, filePath):
        self.text = text
        self.original_interaction = interaction
        self.user = interaction.user.mention
        self.filePath = filePath
        super().__init__()
    
    @discord.ui.button(label="Save to chat", style=discord.ButtonStyle.primary)
    async def buttoncallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.original_interaction.delete_original_response()
        return_text = f"(original message sent by {self.user}) \n" + self.text
        await interaction.response.send_message(return_text, file=discord.File(self.filePath))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="ssml", description="Test your TTS! You can use plain text, SSML, Bikubot shorthand, or a mix of all of them!")
async def ssml(interaction: discord.Interaction, text: str):
    result = subprocess.run(['node', 'static/js/biku_interface.mjs', text], stdout=subprocess.PIPE).stdout.decode('utf-8')
    p = PollySession(result)
    filePath = p.generateMP3File()
    view = ButtonView(text, interaction, filePath)
    await interaction.response.send_message(text, file=discord.File(filePath), view=view, ephemeral=True)

bot.run(os.environ["SSML_BOT_KEY"])