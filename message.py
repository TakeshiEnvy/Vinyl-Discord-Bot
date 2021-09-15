import discord
from discord.ext import commands
import requests
import json

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get inspired quote from "zenquotes"
    def zenquotes(self):
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        json_data = json.loads(response.text)
        quote = f"'*{json_data[0]['q']}*'**  -  **`{json_data[0]['a']}`"
        return quote
    
    #get insult from "Evil Insult"
    def evilinsult(self):
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json", timeout=3)
        json_data = json.loads(response.text)
        return json_data['insult']

    @commands.command(name='inspire', help='Send inpired quote')
    async def inspire(self, ctx):
        quote = self.zenquotes()
        await ctx.send(quote)
    
    @commands.command(name='insult', help='Send insult')
    async def insult(self, ctx):
        quote = self.evilinsult()
        await ctx.send(f'😈 : {quote}')
    
    @commands.command(name='user', help='Display info of tagged person')
    async def user(self, ctx, member: discord.Member):
        embedVar = discord.Embed(title=member.name, description=member.mention, color=discord.Color.green())
        embedVar.add_field(name="ID", value=member.id, inline= True)
        embedVar.set_thumbnail(url=member.avatar_url)
        embedVar.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(message(bot))