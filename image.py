import discord
from discord.ext import commands
import requests
import json
import random

class image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #categories uses to request from "waifu.pics" api
        self.nsfw_categories = ['waifu', 'neko', 'trap', 'blowjob']
        self.sfw_categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']

    #get waifu pics from "waifu.pics"
    def get_waifu_pics(self, type, category):
        url = f'https://api.waifu.pics/{type}/{category}'
        response = requests.get(url)
        json_data = json.loads(response.text)
        return json_data['url']

    @commands.command(name='waifunsfw', help='Send random NSFW waifu pic or gif', aliases=['wnsfw', 'ansfw', 'wn', 'an'])
    async def waifunsfw(self, ctx):
        link = self.get_waifu_pics('nsfw', random.choice(self.nsfw_categories))
        await ctx.send(link)

    @commands.command(name='waifusfw', help='Send random SFW waifu pic or gif', aliases=['wsfw', 'asfw', 'ws', 'as'])
    async def waifusfw(self, ctx):
        link = self.get_waifu_pics('sfw', random.choice(self.sfw_categories))
        await ctx.send(link)

def setup(bot):
    bot.add_cog(image(bot))