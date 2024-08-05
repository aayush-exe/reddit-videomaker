import discord
from discord.ext import commands
from main import *

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='mogus ', intents=intents)

busy = False

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

@bot.command()
async def bogus(ctx):
    #make_money()
    await ctx.send("meow")

@slash.slash(name="custom video", description="Makes video w/ custom characters+plot")
async def ping(ctx: SlashContext, characters: str, plot: str):
    if (busy):
        await ctx.send("making a different video rn, try again in a few mins")
        return
    busy = True
    
    make_money()
    busy = False
    await ctx.send("Video made successfully")



ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())
