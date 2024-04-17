import nextcord
import os

from nextcord import Interaction
from nextcord.ext import commands


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "noplaylist": True,
    "simulate": "True",
    "preferredquality": "192",
    "preferredcodec": "mp3",
    "key": "FFmpegExtractAudio",
}

guild_ids = [
    1090672935255158838,
]


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"{bot.user.name} has connected to Discord.")


@bot.command(name="disconnect")
async def disconect(ctx):
    print(type(ctx))
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.message.reply(f"🍺 Ушёл в запой вместе с {ctx.message.author.mention} 🍺")
    else:
        await ctx.message.reply("Вы попытались разбудить бота, но он в отключке 💤")


@bot.slash_command(name="connect", description="Connects the bot in the voice channel", guild_ids=guild_ids)
async def disconect(interaction: Interaction):
    try:
        vc = interaction.user.voice.channel
        await vc.connect()
        await interaction.send("con")
    except Exception as e:
        await interaction.send("You are not in voice channel")


@bot.slash_command(name="disconnect", description="Disconnects the bot from the voice channel", guild_ids=guild_ids)
async def disconect(interaction: Interaction):
    try:
        await interaction.guild.voice_client.disconnect()
        await interaction.send("discon")
    except Exception as e:
        await interaction.send("You are not in voice channel")


@bot.slash_command(name="play-url", description="PLay song with URL")
async def play_url(interaction: Interaction, url: str):
    return


if __name__ == "__main__":
    bot.run(os.getenv("DISCOR_BOT_TOKEN"))
