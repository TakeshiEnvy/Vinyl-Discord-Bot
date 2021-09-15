import discord
from discord import embeds
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

import music
import message
import anime
import config

cogs = [music, message, anime]

bot = commands.Bot(command_prefix=config.prefix, intents = discord.Intents.all())
bot.remove_command("help")

load_dotenv()

for i in range(len(cogs)):
    cogs[i].setup(bot)

@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + 'online')

@bot.command(name='restart', help="Restart the bot's script", aliases=['reboot'])
async def restart(ctx):
    await ctx.send('🔄 **Restarting bot...**')
    print('Restarting bot...')
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.group(invoke_without_command=True)
async def help(ctx):
    embedVar = discord.Embed(title="Help", description=f"Use `{config.prefix}help` <command> for extended information on a command.", color=discord.Color.green())
    embedVar.add_field(name="Music", value="`play` `join` `leave` `pause` `resume` `skip` `queue` `clear` `remove` `info` `rickroll`")
    embedVar.add_field(name="Anime", value="`anime` `manga` `character` `seiyuu` `staff` `waifu` `lewd`")
    embedVar.add_field(name="Message", value="`inspire` `insult` ")
    await ctx.send(embed=embedVar)

@help.command()
async def anime(ctx):
    embedVar = discord.Embed(title="Anime", description="Search for anime.\n**Alias:** `a`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}anime` <anime's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def manga(ctx):
    embedVar = discord.Embed(title="Manga", description="Search for manga.\n**Alias:** `m`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}manga` <manga's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def character(ctx):
    embedVar = discord.Embed(title="Character", description=f"Search for characters in anime/manga.\nUse `anime` or `manga` before this command.\n**Alias:** `char`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}character` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"<main> <support>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def staff(ctx):
    embedVar = discord.Embed(title="Staff", description="Search for anime's staff.\nUse `anime` before this command.\n**Alias:** `stf`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}staff`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def seiyuu(ctx):
    embedVar = discord.Embed(title="Seiyuu", description="Search for anime's seiyuu.\nUse `anime` before this command.\n**Alias:** `Sei`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}seiyuu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"<main> <support>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def waifu(ctx):
    embedVar = discord.Embed(title="Waifu", description="Send random anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}waifu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| waifu | neko | shinobu | megumin | bully | cuddle | cry | hug | awoo | kiss | lick | pat | smug | bonk | yeet | blush | smile | wave | highfive | handhold | nom | bite | glomp | slap | kill | kick | happy | wink | poke | dance | cringe |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def lewd(ctx):
    embedVar = discord.Embed(title="Lewd", description="Send random hentai anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}lewd` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| waifu | neko | trap | blowjob |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def inspire(ctx):
    embedVar = discord.Embed(title="Inspire", description="Send inpired quote.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}inspire`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def insult(ctx):
    embedVar = discord.Embed(title="Insult", description="Send insult.\nMention people for targeted attack.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}insult`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def user(ctx):
    embedVar = discord.Embed(title="User", description="Display info of mentioned person.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}user`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def play(ctx):
    embedVar = discord.Embed(title="Play", description="Play audio from Youtube.\n**Alias:** `p`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}play` <song's name>\n`{config.prefix}play` <youtube link>\n`{config.prefix}play` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def join(ctx):
    embedVar = discord.Embed(title="Join", description="Join a voice channel.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}join`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def leave(ctx):
    embedVar = discord.Embed(title="Leave", description="Leave voice chat.\n**Alias:** `disconnect`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}leave`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def pause(ctx):
    embedVar = discord.Embed(title="Pause", description="Pause music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}pause`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def resume(ctx):
    embedVar = discord.Embed(title="Resume", description="Resume music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}resume`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def skip(ctx):
    embedVar = discord.Embed(title="Skip", description="Skip current song.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}skip`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def queue(ctx):
    embedVar = discord.Embed(title="Queue", description="Display songs in queue.\n**Alias:** `q`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}queue`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def clear(ctx):
    embedVar = discord.Embed(title="Clear", description="Clear ALL songs in queue.\n**Alias:** `clr`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}clear`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def remove(ctx):
    embedVar = discord.Embed(title="Remove", description="Remove ONE song in queue.\n**Alias:** `rm`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}remove` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def info(ctx):
    embedVar = discord.Embed(title="Info", description="Display information of a song in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}info` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def rickroll(ctx):
    embedVar = discord.Embed(title="Rickroll", description="Tag a person to rickroll.\n**Alias:** `rick`", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}rickroll` <tag person>", inline=False)
    await ctx.send(embed=embedVar)

'''
@help.command()
async def (ctx):
    embedVar = discord.Embed(title="", description="\n**Alias:** ``", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}`", inline=False)
    await ctx.send(embed=embedVar)
'''

bot.run(os.getenv('TOKEN'))