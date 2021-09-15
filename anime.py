import discord
from discord.ext import commands
import requests
import json
import random

import config

#categories uses to request from "waifu.pics" api
nsfw_categories = ['waifu', 'neko', 'trap', 'blowjob']
sfw_categories = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle','cry', 'hug', 'awoo', 'kiss',
                    'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile','wave', 'highfive', 'handhold',
                    'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']

class anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #memory for "MyAnimeList" search
        self.info = {}
        self.characters = []
        self.staffs = []
        self.voice_actors = []
        self.type = ''

    #convert argument 'main' and 'support'
    def convert_arg(self, arg):
        if arg == 'main':
            return 'Main'
        elif arg == 'support':
            return 'Supporting'
        return ''
    
    #process voice actor info
    def process_voice_actor(self, item):
        name = item['name'].replace(',', '')
        return {'id': item['mal_id'], 'name': name, 'url': item['url'], 'image': item['image_url'], 'language': item['language']}

    #get waifu pics from "waifu.pics"
    def get_waifu_pics(self, type, category):
        url = f'https://api.waifu.pics/{type}/{category}'
        response = requests.get(url, timeout=3)
        json_data = json.loads(response.text)
        return json_data['url']

    #get anime info from "MyAnimeList"
    def search_anime(self, query):
        #get anime id
        try:
            url = f"https://api.jikan.moe/v3/search/anime?q={query}&limit=1"
            response = requests.get(url, timeout=3)
            json_data = json.loads(response.text)
            info = json_data['results'][0]
        
            url = f"https://api.jikan.moe/v3/anime/{info['mal_id']}"
            response = requests.get(url, timeout=3)
            info = json.loads(response.text)
        except:
            return False

        start = 'N/A' if not info['aired']['from'] else info['aired']['from'][:10]
        end = "N/A" if not info['aired']['to'] else info['aired']['to'][:10]
        synopsis = "N/A" if not info['synopsis'] else info['synopsis']
        synopsis = (info['synopsis'][:600]+ '...') if len(info['synopsis']) > 600 else info['synopsis']
        score = "N/A" if not info['score'] else info['score']
        premiered = 'N/A' if not info['premiered'] else info['premiered']
    
        return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'trailer': info['trailer_url'],
                'title': info['title'], 'type': info['type'], 'source': info['source'], 'start': start, 'end': end, 'score': score,
                'synopsis': synopsis, 'season': premiered, 'studios': info['studios'], 'identify': 'anime'}

    #get manga info from "MyAnimeList"
    def search_manga(self, query):
        try:
            url = f"https://api.jikan.moe/v3/search/manga?q={query}&limit=1"
            response = requests.get(url, timeout=3)
            json_data = json.loads(response.text)
            info = json_data['results'][0]
       
            url = f"https://api.jikan.moe/v3/manga/{info['mal_id']}"
            response = requests.get(url, timeout=3)
            info = json.loads(response.text)
        except:
            return False

        start = "N/A" if not info['published']['from'] else info['published']['from'][:10]
        end = "N/A" if not info['published']['to'] else info['published']['to'][:10]
        synopsis = "N/A" if not info['synopsis'] else info['synopsis']
        synopsis = (info['synopsis'][:600]+ '...') if len(info['synopsis']) > 600 else info['synopsis']
        score = "N/A" if not info['score'] else info['score']

        return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'title': info['title'], 'status': info['status'],
                'score': score, 'start': start, 'end': end, 'synopsis': synopsis, 'type': info['type'], 'authors': info['authors'], 'identify': 'manga'}

    def get_anime_characters_info(self, arg):
        try:
            url = f"https://api.jikan.moe/v3/anime/{self.info['id']}/characters_staff"
            response = requests.get(url, timeout=3)
            json_data = json.loads(response.text)
            info = json_data['characters']
        except:
            return False
        
        self.characters = []
        self.voice_actors = []
        for i in range(0, len(info)):
            voice_actor = []
            for j in range(0, len(info[i]['voice_actors'])):
                if info[i]['voice_actors'][j]['language'] == config.language:
                    temp = self.process_voice_actor(info[i]['voice_actors'][j])
                    voice_actor.append(temp)

            if voice_actor == []:
                voice_actor = 'N/A'

            if arg == '':
                self.characters.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'], 
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role'], 'voice': voice_actor})
            elif info[i]['role'] == arg:
                self.characters.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'], 
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role'], 'voice': voice_actor})
    
    def get_manga_characters_info(self, arg):
        try:
            url = f"https://api.jikan.moe/v3/manga/{self.info['id']}/characters"
            response = requests.get(url, timeout=3)
            json_data = json.loads(response.text)
            info = json_data['characters']
        except:
            return False
            
        self.characters = []
        for i in range(0, len(info)):
            if arg == '':
                self.characters.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role']})
            elif info[i]['role'] == arg:
                self.characters.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role']})

    def get_anime_staffs_info(self):
        try:
            url = f"https://api.jikan.moe/v3/anime/{self.info['id']}/characters_staff"
            response = requests.get(url, timeout=3)
            json_data = json.loads(response.text)
            info = json_data['staff']
        except:
            return False
            
        self.staffs = []
        for i in range(0, len(info)):
            positions = []
            for j in range(0, len(info[i]['positions'])):
                positions.append(info[i]['positions'][j])

            if positions == []:
                positions = 'N/A'

            self.staffs.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                'name': info[i]['name'].replace(',', ''), 'positions': positions})

    #send embed image
    async def embed_image(self, ctx, link, color):
        embedVar = discord.Embed(color=color)
        embedVar.set_image(url=link)
        await ctx.send(embed=embedVar)

    #send embed anime info
    async def embed_anime_info(self, ctx, info, color):
        embedVar = discord.Embed(title=f"**{info['title']}**", url=info['url'], description=f"**Type:** {info['type']}", color=color)
        embedVar.add_field(name="⭐ Score:", value=info['score'], inline=True)
        embedVar.add_field(name="Source:", value=info['source'], inline=True)

        studios = ''
        if info['studios'] != []:
            for i in range(0, len(info['studios'])):
                studios += f"[{info['studios'][i]['name']}]({info['studios'][i]['url']})\n"
        else:
            studios = 'N/A'

        embedVar.add_field(name="Studio(s):", value=studios, inline=True)
        embedVar.add_field(name="Season:", value=info['season'], inline=True)
        embedVar.add_field(name="Start date:", value=info['start'], inline=True)
        embedVar.add_field(name="End:", value=info['end'], inline=True)
        embedVar.add_field(name="Synopsis:", value=info['synopsis'], inline=False)
        embedVar.set_thumbnail(url=info['image'])
        embedVar.set_author(name='ANIME')
        await ctx.send(embed=embedVar)
        
        if info['trailer'] != None:
            i = info['trailer'].find('?')
            info['trailer'] = info['trailer'][:i].replace("embed/", "watch?v=")
            await ctx.send(info['trailer'])

    #send embed manga info
    async def embed_manga_info(self, ctx, info, color):
        embedVar = discord.Embed(title=f"**{info['title']}**", url=info['url'], description=f"**Type:** {info['type']}", color=color)
        embedVar.add_field(name="⭐ Score:", value=info['score'], inline=True)
        embedVar.add_field(name="Status:", value=info['status'], inline=True)

        authors = ''
        if info['authors'] != []:
            for i in range(0, len(info['authors'])):
                authors += f"[{info['authors'][i]['name']}]({info['authors'][i]['url']})\n"
        else:
            authors = 'N/A'

        embedVar.add_field(name="Author(s):", value=authors, inline=True)
        embedVar.add_field(name="Start date:", value=info['start'], inline=True)
        embedVar.add_field(name="End:", value=info['end'], inline=True)
        embedVar.add_field(name="Synopsis:", value=info['synopsis'], inline=False)
        embedVar.set_thumbnail(url=info['image'])
        embedVar.set_author(name="MANGA")

        await ctx.send(embed=embedVar)

    #send embed anime character info
    async def embed_anime_characters_info(self, ctx, info, color):
        embedVar = discord.Embed(title=info['name'], url=info['url'], color=color)
        voice_actors = info['voice']

        if voice_actors != 'N/A':
            voice_actors_name = ''
            for i in range(0, len(voice_actors)):
                voice_actors_name += f"[{voice_actors[i]['name']}]({voice_actors[i]['url']})\n"
            embedVar.add_field(name="Seiyuu:", value=voice_actors_name, inline=True)

        else:
            embedVar.add_field(name="Seiyuu:", value="N/A", inline=True)

        embedVar.add_field(name="Role:", value=info['role'], inline=True)
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

    #send embed manga character info
    async def embed_manga_characters_info(self, ctx, info, color):
        embedVar = discord.Embed(title=info['name'], url=info['url'], description=f"**Role:** {info['role']}", color=color)
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)
        
    #send embed seiyuu info
    async def embed_seiyuu_info(self, ctx, info, color):
        embedVar = discord.Embed(title=info['name'], url=info['url'], color=color)
        embedVar.add_field(name="Voiced:", value=f"[{info['character']}]({info['character_url']})", inline=True)
        embedVar.add_field(name="Role:", value=info['role'], inline=True)
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

    #send embed anime's staff info
    async def embed_anime_staff_info(self, ctx, info, color):
        embedVar = discord.Embed(title=info['name'], url=info['url'], description=f"**ID:** {info['id']}", color=color)
        
        if info['positions'] != 'N/A':
            positions = ''
            for i in range(0, len(info['positions'])):
                positions += f"{info['positions'][i]}\n"

            embedVar.add_field(name="Position(s):", value=positions, inline=True)
        else:
            embedVar.add_field(name="Position(s):", value="N/A", inline=True)

        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)


    @commands.command(name='lewd', help='Send random NSFW waifu pic or gif')
    async def lewd(self, ctx, *, arg=''):
        if arg in nsfw_categories:
            link = self.get_waifu_pics('nsfw', arg)
        else:
            link = self.get_waifu_pics('nsfw', random.choice(nsfw_categories))
        await self.embed_image(ctx, link, config.hentai_color)

    @commands.command(name='waifu', help='Send random SFW waifu pic or gif')
    async def waifu(self, ctx, *, arg=''):
        if arg in sfw_categories:
            link = self.get_waifu_pics('sfw', arg)
        else:
            link = self.get_waifu_pics('sfw', random.choice(sfw_categories))
        await self.embed_image(ctx, link, config.waifu_color)
        
    @commands.command(name='anime', help='Search for anime', aliases=['a'])
    async def anime(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        self.info = self.search_anime(item)
        if not self.info:
            await ctx.send('❌  **- Try again later** ↻')
        else:
            await self.embed_anime_info(ctx, self.info, config.anime_color)

    @commands.command(name='manga', help='Search for manga', aliases=['m'])
    async def manga(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        self.info = self.search_manga(item)
        if not self.info:
            await ctx.send('❌  **- Try again later** ↻')
        else:
            await self.embed_manga_info(ctx, self.info, config.manga_color)
    
    @commands.command(name='character', help='Search for characters in anime', aliases=['char'])
    async def character(self, ctx, *, arg=''):
        if not self.info:
            await ctx.send(f"❌  **- Use '{config.prefix}anime' or '{config.prefix}manga' before this command**")
            return

        arg = self.convert_arg(arg)
        max_characters = config.characters_number
        await ctx.send(f"🔎 **Searching**")

        if self.info['identify'] == 'manga':
            if self.get_manga_characters_info(arg) == False:
                await ctx.send('❌  **- Try again later** ↻')
                return
            else:
                if len(self.characters) < max_characters:
                    max_characters = len(self.characters)
                for i in range(0, max_characters):
                    await self.embed_manga_characters_info(ctx, self.characters[i], config.character_color)

        else:
            if self.get_anime_characters_info(arg) == False:
                await ctx.send('❌  **- Try again later** ↻')
                return
            else:
                if len(self.characters) < max_characters:
                    max_characters = len(self.characters)
                for i in range(0, max_characters):
                    await self.embed_anime_characters_info(ctx, self.characters[i], config.character_color)

    @commands.command(name='staff', help="Search for anime's staff", aliases=['stf'])
    async def staff(self, ctx):
        if not self.info:
            await ctx.send(f"❌  **- Use '{config.prefix}anime' before this command**")
            return

        max_characters = config.characters_number
        await ctx.send(f"🔎 **Searching**")

        if self.get_anime_staffs_info() == False:
            await ctx.send('❌  **- Try again later** ↻')
            return
        else:
            if len(self.staffs) < max_characters:
                max_characters = len(self.staffs)
            for i in range(0, max_characters):
                await self.embed_anime_staff_info(ctx, self.staffs[i], config.staff_color)

    @commands.command(name='seiyuu', help="Search for anime's seiyuu")
    async def seiyuu(self, ctx, *, arg=''):
        if not self.info:
            await ctx.send(f"❌  **- Use '{config.prefix}anime' before this command**")
            return

        arg = self.convert_arg(arg)
        max_characters = config.characters_number
        await ctx.send(f"🔎 **Searching**")

        if self.get_anime_characters_info(arg) == False:
            await ctx.send('❌  **- Try again later** ↻')
            return

        else:
            if len(self.characters) < max_characters:
                max_characters = len(self.characters)
            
            for i in range(0, max_characters):
                for j in range(0, len(self.characters[i]['voice'])):
                    temp = self.characters[i]['voice'][j]
                    temp['character'] = self.characters[i]['name']
                    temp['character_url'] = self.characters[i]['url']
                    temp['character_id'] = self.characters[i]['id']
                    temp['role'] = self.characters[i]['role']
                    await self.embed_seiyuu_info(ctx, temp, config.seiyuu_color)

def setup(bot):
    bot.add_cog(anime(bot))