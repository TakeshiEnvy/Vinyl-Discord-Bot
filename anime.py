import re
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

    #get info from "myanimelist.net"
    def search_anime(self, type, query):
        try:
            url = f"https://api.jikan.moe/v3/search/{type}?q={query}&limit=1"
            response = requests.get(url)
        except:
            return False

        json_data = json.loads(response.text)
        info = json_data['results'][0]

        if type == 'anime' or type == 'manga':
            return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'title': info['title'], 'score': info['score'], 'start': info['start_date'][:10]}

        if type == 'person':
            return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'name': info['name']}

        if type == 'charcter':
            return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'name': info['name']}

    @commands.command(name='waifunsfw', help='Send random NSFW waifu pic or gif', aliases=['wnsfw', 'ansfw', 'wn', 'an'])
    async def waifunsfw(self, ctx):
        link = self.get_waifu_pics('nsfw', random.choice(self.nsfw_categories))
        await ctx.send(link)

    @commands.command(name='waifusfw', help='Send random SFW waifu pic or gif', aliases=['wsfw', 'asfw', 'ws', 'as'])
    async def waifusfw(self, ctx):
        link = self.get_waifu_pics('sfw', random.choice(self.sfw_categories))
        await ctx.send(link)

    @commands.command(name='anime', help='Search for anime', aliases=['a'])
    async def anime(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        info = self.search_anime('anime', item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
        else:
            await ctx.send(info['url'])

    @commands.command(name='manga', help='Search for manga', aliases=['m'])
    async def manga(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        info = self.search_anime('manga', item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
        else:
            await ctx.send(info['url'])

    @commands.command(name='person', help='Search for anime in anime industry', aliases=['pers'])
    async def person(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        info = self.search_anime('person', item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
        else:
            await ctx.send(info['url'])

    @commands.command(name='character', help='Search for character in anime', aliases=['char'])
    async def character(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        info = self.search_anime('character', item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
        else:
            await ctx.send(info['url'])

def setup(bot):
    bot.add_cog(image(bot))