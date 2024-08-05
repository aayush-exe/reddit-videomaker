import discord
from discord.ext import commands


bot = commands.Bot()

@bot.slash_command(
  name="first_slash",
  guild_ids=[836742375577485344]
)
async def first_slash(ctx): 
    await ctx.respond("You executed the slash command!")
    

ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())