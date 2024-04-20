import os
import yt_dlp
import nextcord
import datetime
import lazy_queue

# from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ext.commands import context


DEBUG = True if os.getenv("DEBUG") == "True" else False

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

    if DEBUG:
        print("Debug mode ON")

    print(f"{bot.user.name} has connected to Discord.")


@bot.command(name="connect", aliases=["con", "c", "join", "j"], guild_ids=guild_ids if DEBUG else None)
async def connect_to_vc(interaction: context.Context):
    if interaction.author.voice:
        if not interaction.voice_client:
            await interaction.author.voice.channel.connect(reconnect=True)
        else:
            await interaction.voice_client.move_to(interaction.author.voice.channel)
    else:
        await interaction.reply("You are not in voice channel")


@bot.command(name="disconnect", aliases=["discon", "d", "off", "kill"], guild_ids=guild_ids if DEBUG else None)
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

    song_url = info["url"]

    name = str(info["title"]).replace("[", "").replace("]", "")
    thumbnail = info.get("thumbnail")
    time = str(datetime.timedelta(seconds=info.get("duration"))) if info.get("duration") else "Прямой эфир"

    embed_url = info.get("original_url")  # "https://youtu.be/" + str(info["id"])

    songs_queue.add([name, time, song_url, embed_url])

    embed = nextcord.Embed(description=f"Записываю [{name}]({embed_url}) в очередь 📝", colour=nextcord.Colour.red())
    embed.add_field(name="Длительность", value=time)
    embed.set_thumbnail(thumbnail)

    try:
        await interaction.message.reply(embed=embed)
    except:
        await interaction.send(embed=embed)


def step_and_remove(voice_client):
    if loop_flag:
        current_queue = songs_queue.get_songs()
        if len(current_queue):
            songs_queue.add(current_queue[0])
    songs_queue.remove()
    audio_player_task(voice_client)


def audio_player_task(voice_client):
    if not voice_client.is_playing() and songs_queue.get_songs():
        voice_client.play(
            nextcord.FFmpegPCMAudio(
                executable="ffmpeg",
                source=songs_queue.get_songs()[0][2],
                **FFMPEG_OPTIONS,
            ),
            after=lambda e: step_and_remove(voice_client),
        )


# ===== Play command staf End =====


@bot.command(name="play", aliases=["p", "pl", "go"], guild_ids=guild_ids if DEBUG else None)
async def play(interaction: context.Context, *url):
    await connect_to_vc(interaction)

    if not url or url == "":
        embed = nextcord.Embed(description="Введите название песни или ссылку на нее", colour=nextcord.Colour.red())
        return await interaction.message.reply(embed=embed)

    await add(interaction, " ".join(url))
    try:
        await interaction.message.add_reaction(emoji="🎸")
    except Exception as err:
        pass

    voice_client = interaction.guild.voice_client
    audio_player_task(voice_client)


@bot.command(name="loop", aliases=["l", "lo", "rp"], guild_ids=guild_ids if DEBUG else None)
async def loop(interaction: context.Context):
    global loop_flag
    loop_flag = True
    await interaction.message.reply("Залуплено")


@bot.command(name="unloop", aliases=["unl", "ul", "ll"], guild_ids=guild_ids if DEBUG else None)
async def unloop(interaction: context.Context):
    global loop_flag
    loop_flag = False
    await interaction.message.reply("Отлуплено")


@bot.command(name="queue", aliases=["q", "qq", "ss", "songs"], guild_ids=guild_ids if DEBUG else None)
async def queue(interaction: context.Context):
    if len(songs_queue.get_songs()) > 0 and len(songs_queue.get_songs()) != 1:
        songs = list()

        for index, song in enumerate(songs_queue.get_songs(), 1):
            name = song[0]
            if len(song[0]) > 30:
                name = song[0][:30] + "..."
            songs.append(f"📀 `{index}. {name:<33}   {song[1]:>20}`\n")

        songs[0] = songs[0].replace("📀", "🎶")  # current song

        embed = nextcord.Embed(
            title=f"Очередь [LOOP: {loop_flag}]",
            description="".join(songs),
            colour=nextcord.Colour.red(),
        )
        await interaction.send(embed=embed)
    else:
        await interaction.send("Очередь пуста 📄")


@bot.command(name="pause", aliases=["ps", "pa", "pp", "stop"], guild_ids=guild_ids if DEBUG else None)
async def pause(interaction: context.Context):
    voice = nextcord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice:
        song = songs_queue.get_songs()[0]
        voice.pause()
        await interaction.message.reply(f"Поставили трек [{song[0]}]({song[2]}) на паузу")


@bot.command(name="resume", aliases=["r", "res", "cont", "ct"], guild_ids=guild_ids if DEBUG else None)
async def resume(interaction: context.Context):
    voice = nextcord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice:
        if voice.is_paused():
            song = songs_queue.get_songs()[0]
            voice.resume()
            await interaction.message.reply(f"Сняли трек [{song[0]}]({song[2]}) с паузы")


@bot.command(name="skip", aliases=["s", "sk", "next", "nx", "nxt"], guild_ids=guild_ids if DEBUG else None)
async def skip(interaction: context.Context):
    voice = nextcord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice:
        songs = songs_queue.get_songs()
        song_now = songs[0]
        if len(songs) > 1:
            song_next = songs[1]
            voice.stop()

            track_now = song_now[0][:33] + "..." if len(song_now[0]) > 33 else song_now[0]
            track_next = song_next[0][:33] + "..." if len(song_next[0]) > 33 else song_next[0]

            embed = nextcord.Embed(
                description=f"Скипаем трек [{track_now}]({song_now[3]}) - {song_now[1]}\nСледующий трек - [{track_next}]({song_next[3]}) - {song_next[1]}",
                colour=nextcord.Colour.red(),
            )
            await interaction.message.reply(embed=embed)
        else:
            voice.stop()


@bot.command(name="clear", aliases=["cl", "cc", "flush", "fl"], guild_ids=guild_ids if DEBUG else None)
async def clear(interaction: context.Context):
    voice = nextcord.utils.get(bot.voice_clients, guild=interaction.guild)
    if voice:
        voice.stop()
        while not songs_queue.is_empty():
            songs_queue.remove()


@bot.command(name="remove", aliases=["rem", "del", "ds", "dd", "rr"], guild_ids=guild_ids if DEBUG else None)
async def remove(interaction: context.Context, index: int):
    try:
        if len(songs_queue.get_songs()):
            if index - 1 >= 0:
                removed_song = songs_queue.remove_by_index(index - 1)
                await interaction.message.reply(f"Вычеркнул из списка: ({removed_song[0]})[{removed_song[3]}]")
        else:
            await interaction.message.reply("Нечего удалять")
    except:
        await interaction.message.reply(f"Песни с такой позицией не существует")


if __name__ == "__main__":
    bot.run(os.getenv("DISCOR_BOT_TOKEN"))
