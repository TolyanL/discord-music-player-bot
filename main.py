import nextcord
import os

from nextcord import Interaction
from nextcord.ext import commands


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"{bot.user.name} has connected to Discord.")


if __name__ == "__main__":
    bot.run(os.getenv("DISCOR_BOT_TOKEN"))
