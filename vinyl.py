import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys

import music
import message
import anime
import config

load_dotenv()
cogs = [music, message, anime]

bot = commands.Bot(command_prefix=config.prefix, intents = discord.Intents.all())
bot.remove_command("help")

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
    embedVar.add_field(name="Anime", value="`anime` `manga` `character` `seiyuu` `staff` `waifu` `lewd` `aniquote`")
    embedVar.add_field(name="Message", value="`inspire` `insult` `ping` `qrcode`")
    await ctx.send(embed=embedVar)

@help.command(aliases=['a'])
async def anime(ctx):
    embedVar = discord.Embed(title="Anime", description="__Alias__ : `a`\n- Search for anime.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}anime` <anime's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['m'])
async def manga(ctx):
    embedVar = discord.Embed(title="Manga", description="__Alias__ : `m`\n- Search for manga.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}manga` <manga's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['char'])
async def character(ctx):
    embedVar = discord.Embed(title="Character", description=f"__Alias__ : `char`\n- Search for characters in anime/manga.\n- Use `anime` or `manga` before this command to search for characters in specific anime/manga.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}character` <name>\n`{config.prefix}character` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| main | support |", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['stf'])
async def staff(ctx):
    embedVar = discord.Embed(title="Staff", description="__Alias__ : `stf`\n- Search for anime's staff.\n- Use `anime` before this command.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}staff`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['sei'])
async def seiyuu(ctx):
    embedVar = discord.Embed(title="Seiyuu", description="__Alias__ : `sei`\n- Search for anime's seiyuu.\n- Use `anime` before this command.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}seiyuu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| main | support |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def waifu(ctx):
    options = '|'
    for i in range (0, len(config.waifu_categories)):
        options += f" {config.waifu_categories[i]} |"
    embedVar = discord.Embed(title="Waifu", description="- Send random anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}waifu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| waifu | neko | shinobu | megumin | bully | cuddle | cry | hug | awoo | kiss | lick | pat | smug | bonk | yeet | blush | smile | wave | highfive | handhold | nom | bite | glomp | slap | kill | kick | happy | wink | poke | dance | cringe |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def lewd(ctx):
    options = '|'
    for i in range (0, len(config.hentai_categories)):
        options += f" {config.hentai_categories[i]} |"
    embedVar = discord.Embed(title="Lewd", description="- Send random hentai anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}lewd` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=options, inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['aquote', 'aq'])
async def aniquote(ctx):
    embedVar = discord.Embed(title="Aniquote", description="__Alias__ : `aquote` `aq`\n- Send random anime quote.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}aniquote`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def inspire(ctx):
    embedVar = discord.Embed(title="Inspire", description="- Send inpired quote.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}inspire`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def insult(ctx):
    embedVar = discord.Embed(title="Insult", description="Send insult.\n- Mention people for targeted attack.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}insult`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def ping(ctx):
    embedVar = discord.Embed(title="Ping", description="- Display bot's latency.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}ping`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['qr'])
async def qrcode(ctx):
    embedVar = discord.Embed(title="Qrcode", description="__Alias__ : `qr`\n- Create QR code.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}qrcode` <item>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['p'])
async def play(ctx):
    embedVar = discord.Embed(title="Play", description="__Alias__ : `p`\n- Play audio from Youtube.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}play` <song's name>\n`{config.prefix}play` <youtube link>\n`{config.prefix}play` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def join(ctx):
    embedVar = discord.Embed(title="Join", description="- Join a voice channel.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}join`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['disconnect'])
async def leave(ctx):
    embedVar = discord.Embed(title="Leave", description="__Alias__ : `disconnect`\n- Leave voice chat.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}leave`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def pause(ctx):
    embedVar = discord.Embed(title="Pause", description="- Pause music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}pause`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def resume(ctx):
    embedVar = discord.Embed(title="Resume", description="- Resume music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}resume`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['next'])
async def skip(ctx):
    embedVar = discord.Embed(title="Skip", description="__Alias__ : `next`\n- Skip current song.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}skip`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['q'])
async def queue(ctx):
    embedVar = discord.Embed(title="Queue", description="__Alias__ : `q`\n- Display songs in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}queue`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['clr'])
async def clear(ctx):
    embedVar = discord.Embed(title="Clear", description="__Alias__ : `clr`\n- Clear ALL songs in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}clear`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['rm'])
async def remove(ctx):
    embedVar = discord.Embed(title="Remove", description="__Alias__ : `rm`\n- Remove ONE song in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}remove` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def info(ctx):
    embedVar = discord.Embed(title="Info", description="- Display information of a song in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}info` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['rick'])
async def rickroll(ctx):
    embedVar = discord.Embed(title="Rickroll", description="__Alias__ : `rick`\n- Tag a person to rickroll.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{config.prefix}rickroll` <tag person>", inline=False)
    await ctx.send(embed=embedVar)

bot.run(os.getenv('TOKEN'))