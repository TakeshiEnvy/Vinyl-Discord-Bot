import discord
from discord.ext import commands
import requests
import json

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get inspired quote from "zenquotes"
    def zenquotes(self):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = f"'*{json_data[0]['q']}*'**  -  **`{json_data[0]['a']}`"
        return quote
    
    #get insult from "Evil Insult"
    def evilinsult(self):
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        json_data = json.loads(response.text)
        quote = json_data['insult']
        return quote

    #send inpired quote
    @commands.command(name='inspire', help='Send inpired quote')
    async def inspire(self, ctx):
        quote = self.zenquotes()
        await ctx.send(quote)
    
    #send insult
    @commands.command(name='insult', help='Send insult')
    async def insult(self, ctx):
        quote = self.evilinsult()
        await ctx.send(f'😈 : {quote}')

def setup(bot):
    bot.add_cog(message(bot))