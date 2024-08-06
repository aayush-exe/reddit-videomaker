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
    guild_ids=[836742375577485344, 933924457079275540]
)
async def create_video(
  ctx, 
  characters: discord.Option(str, "Separate characters with comma, you can include character traits in paranthesis", required=True),
  plot_description: discord.Option(str, "General plot of story or specific plot points you want to include", required=True)): 
    global busy
    if busy:
        await ctx.response.send_message("Making a different video rn, try again in a few mins")
        return
    busy = True
    await ctx.respond("Starting generation (this may take a couple minutes)")
    
    set_username(ctx.user.name)
    get_openai_response(characters=characters, plot=plot_description)
    youtube_link = make_money(1).strip()

    
    
    embed = discord.Embed(
        title="Video from @"+ctx.user.name,
        description="Thanks for using mogusbogusmeow",
        color=0x00ff00  # You can customize the color
    )
    
    # Replace 'FILE_ID' with the actual ID of your video file
    embed.add_field(name="epic video!!1!", value=f"[Click to view]({youtube_link})")
    await ctx.respond(embed=embed)
        
    # await ctx.respond("Link: "+youtube_link)
    busy = False
    

ffile = open('data/secret.txt', 'r')

bot.run(ffile.readline().strip())
