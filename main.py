import os
import yt_dlp
import nextcord
import datetime
import lazy_queue


# from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import context


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents)

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

songs_queue = lazy_queue.Queue()
loop_flag = True

guild_ids = [
    1090672935255158838,
]


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"{bot.user.name} has connected to Discord.")


@bot.command(name="connect", guild_ids=guild_ids, aliases=["con", "c", "join", "j"])
async def connect_to_vc(interaction: context.Context):
    if interaction.author.voice:
        if not interaction.voice_client:
            await interaction.author.voice.channel.connect(reconnect=True)
        else:
            await interaction.voice_client.move_to(interaction.author.voice.channel)
    else:
        await interaction.reply("You are not in voice channel")


@bot.command(name="disconnect", guild_ids=guild_ids, aliases=["discon", "d", "off", "kill"])
async def disconect_to_vc(interaction: context.Context):
    if interaction.voice_client:
        await interaction.guild.voice_client.disconnect()
    else:
        await interaction.reply("You are not in voice channel")


# ===== Play command staf =====


async def add(interaction: context.Context, url: str):
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except:
            info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]

    name = info["title"]
    time = str(datetime.timedelta(seconds=info["duration"]))

    songs_queue.add([name, time, info["url"]])

    embed = nextcord.Embed(description=f"Записываю [{name}]({url}) в очередь 📝", colour=nextcord.Colour.red())
    await interaction.message.reply(embed=embed)


def step_and_remove(voice_client):
    if loop_flag:
        songs_queue.add(songs_queue.get_value()[0])
    songs_queue.q_remove()
    audio_player_task(voice_client)


def audio_player_task(voice_client):
    if not voice_client.is_playing() and songs_queue.get_value():
        voice_client.play(
            nextcord.FFmpegPCMAudio(
                executable="ffmpeg",
                source=songs_queue.get_value()[0][2],
                **FFMPEG_OPTIONS,
            ),
            after=lambda e: step_and_remove(voice_client),
        )


# ===== Play command staf End =====


@bot.command(name="play", guild_ids=guild_ids, aliases=["p", "s", "pl", "go"])
async def play(interaction: context.Context, *url):
    await connect_to_vc(interaction)

    await add(interaction, " ".join(url))
    await interaction.message.add_reaction(emoji="🎸")

    voice_client = interaction.guild.voice_client
    audio_player_task(voice_client)


if __name__ == "__main__":
    bot.run(os.getenv("DISCOR_BOT_TOKEN"))

# https://youtu.be/a_0DF6xolfA?si=MO7PNWMiAMQIY_ZE
