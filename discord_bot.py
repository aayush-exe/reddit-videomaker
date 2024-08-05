import discord
from discord import app_commands
from discord.ext import commands
from main import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='mogus ', intents=intents)

busy = False

guildID = 836742375577485344

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

@bot.command()
async def bogus(ctx):
    #make_money()
    await ctx.send("meow")

@tree.command(
    name="custom_video", 
    description="Makes video w/ custom characters+plot",
    guild=discord.Object(id=12417128931)
)
@app_commands.describe(characters="Characters for the video", plot="Plot for the video")
async def gen_video(interaction: discord.Interaction, characters: str, plot: str):
    global busy
    if busy:
        await interaction.response.send_message("Making a different video rn, try again in a few mins")
        return

    busy = True

    # Placeholder functions for your actual implementation
    def set_username(username):
        print(f"Username set to: {username}")

    def make_money():
        print("Making money...")

    set_username(interaction.user.name)
    make_money()

    busy = False
    await interaction.response.send_message("Video made successfully")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=12417128931))
    print("Synced")
    

ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())
