import discord
from discord.ext import commands
from main import *
from openai_custom import *


bot = commands.Bot()

busy = False

@discord.option("first", type=discord.SlashCommandOptionType.string) # type = str also works
@discord.option("second", type=discord.SlashCommandOptionType.string) # type = str also works

@bot.slash_command(
   name="custom_video",
    description="Add custom characters, character traits, and plot",
    guild_ids=[836742375577485344]
)
async def create_video(
  ctx, 
  characters: discord.Option(str, "Separate characters with comma, you can include character traits in paranthesis", required=True),
  plot_description: discord.Option(str, "General plot of story or specific plot points you want to include", required=True)): 
    global busy
    if busy:
        await ctx.response.send_message("Making a different video rn, try again in a few mins")
        return
    await ctx.respond("Starting generation (this may take a couple minutes)")
    busy = True
    set_username(ctx.user.name)
    get_openai_response(characters=characters, plot=plot_description)
    make_money(1)
    await ctx.respond("It's finished! Link: ")
    busy = False
    await ctx.response.send_message("Video made successfully")
    

ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())