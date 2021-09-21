import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, sys, json

import music, anime, message

load_dotenv()

with open("config.json", 'r') as file:
    data = json.load(file)
    file.close()
Prefix = data['MAIN']['prefix']

bot = commands.Bot(command_prefix=Prefix, intents = discord.Intents.all())
bot.remove_command("help")

bot.add_cog(music.Music(bot))
bot.add_cog(anime.Anime(bot))
bot.add_cog(message.Message(bot))

@bot.event
async def on_ready():
    print(f"Bot {bot.user} online")

@bot.command(name='restart', help="Restart the bot's script", aliases=['reboot'])
async def restart(ctx):
    await ctx.send('🔄 **Restarting bot...**')
    print('Restarting bot...')
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.group(invoke_without_command=True)
async def help(ctx):
    embedVar = discord.Embed(title="Help", description=f"Use `{Prefix}help` <command> for extended information on a command.", color=discord.Color.green())
    embedVar.add_field(name="Music", value="`play`  `join`  `leave`  `pause`  `resume`  `skip`  `queue`  `clear`  `remove`  `info`  `loop`  `loopoff`  `rickroll`")
    embedVar.add_field(
        name="Anime", value="`anime`  `manga`  `character`  `seiyuu`  `staff`  `waifu`  `lewd`  `nhentai`  `aniquote`  `set_lewd`  `set_lewd_off`")
    embedVar.add_field(name="Message", value="`inspire`  `insult`  `ping`  `qrcode`")
    await ctx.send(embed=embedVar)

@help.command(aliases=['a', 'ani'])
async def anime(ctx):
    embedVar = discord.Embed(title="Anime", description="__Alias__ : `a`  `ani`\n- Search for anime.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}anime` <anime's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['m'])
async def manga(ctx):
    embedVar = discord.Embed(title="Manga", description="__Alias__ : `m`\n- Search for manga.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}manga` <manga's name>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['char'])
async def character(ctx):
    embedVar = discord.Embed(title="Character", description=f"__Alias__ : `char`\n- Search for characters in anime/manga.\n- Use `anime` or `manga` before this command to search for characters in specific anime/manga.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}character` <name>\n`{Prefix}character` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| main | support |", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['stf'])
async def staff(ctx):
    embedVar = discord.Embed(title="Staff", description="__Alias__ : `stf`\n- Search for anime's staff.\n- Use `anime` before this command.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}staff`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['sei'])
async def seiyuu(ctx):
    embedVar = discord.Embed(title="Seiyuu", description="__Alias__ : `sei`\n- Search for anime's seiyuu.\n- Use `anime` before this command.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}seiyuu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| main | support |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def waifu(ctx):
    options = '|'
    for i in range (0, len(data['ANIME']['waifu_categories'])):
        options += f" {data['ANIME']['waifu_categories'][i]} |"
    embedVar = discord.Embed(title="Waifu", description="- Send random anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}waifu` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=f"| waifu | neko | shinobu | megumin | bully | cuddle | cry | hug | awoo | kiss | lick | pat | smug | bonk | yeet | blush | smile | wave | highfive | handhold | nom | bite | glomp | slap | kill | kick | happy | wink | poke | dance | cringe |", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def lewd(ctx):
    options = '|'
    for i in range(0, len(data['ANIME']['hentai_categories'])):
        options += f" {data['ANIME']['hentai_categories'][i]} |"
    embedVar = discord.Embed(title="Lewd", description="- Send random hentai anime pic or gif.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}lewd` <optional>", inline=False)
    embedVar.add_field(name="Options:", value=options, inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def set_lewd(ctx):
    embedVar = discord.Embed(title="Set_lewd", description="- Set a channel to send random hentai anime pic or gif at specific time.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}set_lewd` <time>", inline=False)
    embedVar.add_field(name="Example:", value=f"`{Prefix}set_lewd` 21:32", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def set_lewd_off(ctx):
    embedVar = discord.Embed(title="Set_lewd_off", description="- Turn off `set_lewd`.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}set_lewd_off`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['aquote', 'aq'])
async def aniquote(ctx):
    embedVar = discord.Embed(title="Aniquote", description="__Alias__ : `aquote` `aq`\n- Send random anime quote.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}aniquote`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['ntai'])
async def nhentai(ctx):
    embedVar = discord.Embed(title="Nhentai", description="__Alias__ : `ntai`\n- Find information about 'cultured' digits.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}nhentai` <digits>", inline=False)
    await ctx.send(embed=embedVar)

#=====================================================================================================================================================
@help.command()
async def inspire(ctx):
    embedVar = discord.Embed(title="Inspire", description="- Send inpired quote.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}inspire`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def insult(ctx):
    embedVar = discord.Embed(title="Insult", description="Send insult.\n- Mention people for targeted attack.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}insult`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def ping(ctx):
    embedVar = discord.Embed(title="Ping", description="- Display bot's latency.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}ping`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['qr'])
async def qrcode(ctx):
    embedVar = discord.Embed(title="Qrcode", description="__Alias__ : `qr`\n- Create QR code.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}qrcode` <item>", inline=False)
    await ctx.send(embed=embedVar)

#=====================================================================================================================================================
@help.command(aliases=['p'])
async def play(ctx):
    embedVar = discord.Embed(title="Play", description="__Alias__ : `p`\n- Play audio from Youtube.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}play` <song's name>\n`{Prefix}play` <youtube link>\n`{Prefix}play` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def join(ctx):
    embedVar = discord.Embed(title="Join", description="- Join a voice channel.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}join`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['disconnect'])
async def leave(ctx):
    embedVar = discord.Embed(title="Leave", description="__Alias__ : `disconnect`\n- Leave voice chat.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}leave`", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def pause(ctx):
    embedVar = discord.Embed(title="Pause", description="- Pause music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}pause`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['res'])
async def resume(ctx):
    embedVar = discord.Embed(title="Resume", description="__Alias__ : `res`\n- Resume music.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}resume`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['next'])
async def skip(ctx):
    embedVar = discord.Embed(title="Skip", description="__Alias__ : `next`\n- Skip current song.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}skip`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['q'])
async def queue(ctx):
    embedVar = discord.Embed(title="Queue", description="__Alias__ : `q`\n- Display songs in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}queue`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['clr'])
async def clear(ctx):
    embedVar = discord.Embed(title="Clear", description="__Alias__ : `clr`\n- Clear ALL songs in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}clear`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['rm'])
async def remove(ctx):
    embedVar = discord.Embed(title="Remove", description="__Alias__ : `rm`\n- Remove ONE song in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}remove` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command()
async def info(ctx):
    embedVar = discord.Embed(title="Info", description="- Display information of a song in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}info` <queue number>", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['repeat'])
async def loop(ctx):
    embedVar = discord.Embed(title="Loop", description="__Alias__ : `repeat`\n- Loop songs in queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}loop`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['repeatoff', 'loff', 'roff'])
async def loopoff(ctx):
    embedVar = discord.Embed(title="Loopoff", description="__Alias__ : `repeatoff`  `loff`  `roff`\n- Stop looping queue.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}loopoff`", inline=False)
    await ctx.send(embed=embedVar)

@help.command(aliases=['rick'])
async def rickroll(ctx):
    embedVar = discord.Embed(title="Rickroll", description="__Alias__ : `rick`\n- Tag a person to rickroll.", color=discord.Color.green())
    embedVar.add_field(name="Syntax:", value=f"`{Prefix}rickroll` <tag person>", inline=False)
    await ctx.send(embed=embedVar)

bot.run(os.getenv('TOKEN'))
