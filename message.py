import discord
from discord.ext import commands
import requests
import json

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get inspired quote from "zenquotes"
    def zenquotes(self):
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=3)
            json_data = json.loads(response.text)
            quote = f"'*{json_data[0]['q']}*'**  -  **`{json_data[0]['a']}`"
            return quote
        except:
            return False
    
    #get insult from "Evil Insult"
    def evilinsult(self):
        try:
            response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json", timeout=3)
            json_data = json.loads(response.text)
            return json_data['insult']
        except:
            return False

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

def setup(bot):
    bot.add_cog(message(bot))