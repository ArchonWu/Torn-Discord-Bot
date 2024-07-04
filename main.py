import discord
import os
from dotenv import load_dotenv
from discord.ext import bridge

load_dotenv()
intents = discord.Intents.all()

TOKEN = os.getenv('DISCORD_TOKEN')
bot = bridge.Bot(command_prefix='!', intents=intents)
bot.token = TOKEN


# Loops through all .py files in the 'Cogs' folder and loads them (e.g. Loops)
for file in os.listdir(f"Cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"Cogs.{file[:-3]}")
    print(file)


# bot start up
@bot.event
async def on_ready():
    # Updates Bot Activity
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"Torn Stats"))

    print("torn_bot running!")


# runs the bot
bot.run(bot.token, reconnect=True)

