import discord
from discord.ext import commands
from main import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='mogus ', intents=intents)

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

@bot.command()
async def bogus(ctx):
    make_money()
    await ctx.send("Did it on someone's computer")

ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())
