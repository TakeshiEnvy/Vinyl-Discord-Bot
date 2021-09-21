import discord
from discord.ext import commands
import qrcode
import requests
import json

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json", 'r') as file:
            data = json.load(file)
            file.close()
        self.cfg = data['MESSAGE']

    #get inspired quote from "zenquotes"
    def zenquotes(self):
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=self.cfg['timeout'])
            json_data = json.loads(response.text)
            quote = f"'*{json_data[0]['q']}*'\n> **{json_data[0]['a']}**"
            return quote
        except:
            return False
    
    #get insult from "Evil Insult"
    def evilinsult(self):
        try:
            response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json", timeout=self.cfg['timeout'])
            json_data = json.loads(response.text)
            return json_data['insult']
        except:
            return False

#================================================================================================================================================

    @commands.command(name='inspire', help='Send inpired quote')
    async def inspire(self, ctx):
        quote = self.zenquotes()
        if not quote:
            await ctx.send("❌  **- Error**")
        else:
            await ctx.send(quote)
    
    @commands.command(name='insult', help='Send insult')
    async def insult(self, ctx):
        quote = self.evilinsult()
        if not quote:
            await ctx.send("❌  **- Error**")
        else:
            await ctx.send(f'😈 : {quote}')
    
    @commands.command(name='ping', help="Measure bot's latency")
    async def ping(self, ctx):
        await ctx.send(f'**Pong!** `{round(self.bot.latency * 1000)}ms`')
    
    @commands.command()
    async def image(self, ctx):
        #await ctx.send("D:\Code\Vinyl-Discord-Bot\data\emotes\AquaBaka.png")
        await ctx.send(file=discord.File('./data/emotes/AquaBaka.png'))
    
    @commands.command(name="qrcode", help="Create qr code", aliases=['qr'])
    async def qrcode(self, ctx, *items):
        item = ' '.join(items)
        cfg = self.cfg['qrcode']
        qr = qrcode.QRCode(
            version = cfg['version'],
            error_correction = qrcode.constants.ERROR_CORRECT_M,
            box_size = cfg['box_size'],
            border = cfg['border']
        )
        qr.add_data(item)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color = tuple(cfg['qr_foreground']),
            back_color = tuple(cfg['qr_background'])
        )

        with open('data/qrcode.png', 'wb') as file:
            img.save(file)
        await ctx.send(file=discord.File('data/qrcode.png'))
