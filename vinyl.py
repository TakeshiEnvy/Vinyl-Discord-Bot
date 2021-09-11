import discord
from discord.ext import commands
import os
import sys
import music
import message
import image

cogs = [music, message, image]

bot = commands.Bot(command_prefix=">", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + 'online')

@bot.command(name='restart', help="Restart the bot's script", aliases=['reboot'])
async def restart(ctx):
    await ctx.send('🔄 **Restarting bot...**')
    os.execv(sys.executable, ['python'] + sys.argv)

for i in range(len(cogs)):
    cogs[i].setup(bot)

#get token
with open("token.txt") as file:
    TOKEN = file.read()
bot.run(TOKEN)
