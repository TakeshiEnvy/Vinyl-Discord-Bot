import discord
from discord.ext import commands
import os
import sys
import music
import message

cogs = [music, message]

bot = commands.Bot(command_prefix=">", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Bot {0.user} '.format(bot) + 'online')

@bot.command(name='restart', help="Restart the bot's script", aliases=['reboot'])
async def restart(ctx):
    await ctx.send('🔄 **Restarting bot...**')
    print('Restarting bot...')
    os.execv(sys.executable,['python'] + sys.argv)

for i in range(len(cogs)):
    cogs[i].setup(bot)

#get token
bot.run('ODg0NzM5NzU5ODY2NTExMzkw.YTc4HA.wEiy1ru4TLCJhy-56YAehrLP0gU')