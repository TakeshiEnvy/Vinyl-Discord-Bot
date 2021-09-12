import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sys
import music
import message
import anime

cogs = [music, message, anime]

bot = commands.Bot(command_prefix=">", intents = discord.Intents.all())

load_dotenv()

@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + 'online')
'''
@bot.event
async def on_message(message):
    if message.content.startswith('!hello'):
        embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        embedVar.add_field(name="Field1", value="hi", inline=False)
        embedVar.add_field(name="Field2", value="hi2", inline=False)
        await message.channel.send(embed=embedVar)
'''
@bot.command(name='restart', help="Restart the bot's script", aliases=['reboot'])
async def restart(ctx):
    await ctx.send('🔄 **Restarting bot...**')
    print('Restarting bot...')
    os.execv(sys.executable, ['python'] + sys.argv)

for i in range(len(cogs)):
    cogs[i].setup(bot)

#get token
bot.run(os.getenv('TOKEN'))