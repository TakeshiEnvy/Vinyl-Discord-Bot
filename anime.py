import discord
from discord.ext import commands, tasks
from hentai import Hentai, Format, Tag
from datetime import datetime
import requests
import random, json

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json", 'r') as file:
            data = json.load(file)
            file.close()
        self.cfg = data['ANIME']

        self.background_lewd.start()

        #memory for "MyAnimeList" search
        self.info = {}
        self.characters_staff = []
        self.voice_actors = []
        self.type = ''
        self.previous_command = ''

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
        try:
            url = f'https://waifu.pics/api/{type}/{category}'
            response = requests.get(url, timeout=self.cfg['timeout'])
            json_data = json.loads(response.text)
            return json_data['url']
        except:
            return False

    #get anime quote from "AnimeChan"
    def get_anime_quote(self):
        try:
            url = f'https://animechan.vercel.app/api/random'
            response = requests.get(url, timeout=self.cfg['timeout'])
            json_data = json.loads(response.text)
            quote = f"*'{json_data['quote']}'*\n> **{json_data['character']}** - `{json_data['anime']}`"
            return quote
        except:
            return False

    #earch anime/manga info from "MyAnimeList"
    def search(self, type, query):
        try:
            url = f"https://api.jikan.moe/v3/search/{type}?q={query}&limit=1"
            response = requests.get(url, timeout=self.cfg['mal_timeout'])
            json_data = json.loads(response.text)
            info = json_data['results'][0]
       
            url = f"https://api.jikan.moe/v3/{type}/{info['mal_id']}"
            response = requests.get(url, timeout=self.cfg['mal_timeout'])
            info = json.loads(response.text)
        except:
            return False

        
        synopsis = "N/A" if not info['synopsis'] else info['synopsis']
        synopsis = (info['synopsis'][:600]+ '...') if len(info['synopsis']) > 600 else info['synopsis']
        score = "N/A" if not info['score'] else info['score']

        if type == 'anime':
            start = 'N/A' if not info['aired']['from'] else info['aired']['from'][:10]
            end = "N/A" if not info['aired']['to'] else info['aired']['to'][:10]
            premiered = 'N/A' if not info['premiered'] else info['premiered']

            return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'trailer': info['trailer_url'],
                    'title': info['title'], 'type': info['type'], 'source': info['source'], 'start': start, 'end': end, 'score': score,
                    'synopsis': synopsis, 'season': premiered, 'studios': info['studios'], 'identify': 'anime'}
         
        if type == 'manga':
            start = "N/A" if not info['published']['from'] else info['published']['from'][:10]
            end = "N/A" if not info['published']['to'] else info['published']['to'][:10]

            return {'id': info['mal_id'], 'url': info['url'], 'image': info['image_url'], 'title': info['title'], 'status': info['status'],
                    'score': score, 'start': start, 'end': end, 'synopsis': synopsis, 'type': info['type'], 'authors': info['authors'], 'identify': 'manga'}

    def search_character(self, query):
        try:
            url = f"https://api.jikan.moe/v3/search/character?q={query}&limit=5"
            response = requests.get(url, timeout=self.cfg['mal_timeout'])
            json_data = json.loads(response.text)
            info = json_data['results']
        except:
            return False

        self.characters_staff = []
        for i in range(0, len(info)):
            self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'], 'manga': info[i]['manga'],
                                        'alter_name': info[i]['alternative_names'], 'name': info[i]['name'].replace(',', ''), 'anime': info[i]['anime']})

    def get_characters_staff_info(self, type, arg):
        try:
            url = f"https://api.jikan.moe/v3/anime/{self.info['id']}/characters_staff"
            response = requests.get(url, timeout=self.cfg['mal_timeout'])
            json_data = json.loads(response.text)
            info = json_data[type]
        except:
            return False

        self.characters_staff = []
        if type == 'characters':
            #process info about anime characters
            self.voice_actors = []
            for i in range(0, len(info)):
                voice_actor = []
                for j in range(0, len(info[i]['voice_actors'])):
                    if info[i]['voice_actors'][j]['language'] == self.cfg['language']:
                        temp = self.process_voice_actor(info[i]['voice_actors'][j])
                        voice_actor.append(temp)

                if arg == '':
                    self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'], 
                                                'name': info[i]['name'].replace(',', ''), 'role': info[i]['role'], 'voice': voice_actor})
                elif info[i]['role'] == arg:
                    self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'], 
                                                'name': info[i]['name'].replace(',', ''), 'role': info[i]['role'], 'voice': voice_actor})
        else:
            #process info about anime staff
            for i in range(0, len(info)):
                positions = []
                for j in range(0, len(info[i]['positions'])):
                    positions.append(info[i]['positions'][j])

                self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                            'name': info[i]['name'].replace(',', ''), 'positions': positions})
    
    def get_manga_characters_info(self, arg):
        try:
            url = f"https://api.jikan.moe/v3/manga/{self.info['id']}/characters"
            response = requests.get(url, timeout=self.cfg['mal_timeout'])
            json_data = json.loads(response.text)
            info = json_data['characters']
        except:
            return False
            
        self.characters_staff = []
        for i in range(0, len(info)):
            if arg == '':
                self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role']})
            elif info[i]['role'] == arg:
                self.characters_staff.append({'id': info[i]['mal_id'], 'url': info[i]['url'], 'image': info[i]['image_url'],
                                        'name': info[i]['name'].replace(',', ''), 'role': info[i]['role']})

    #send embed image
    async def embed_image(self, message_channel, link, color):
        embedVar = discord.Embed(color=color)
        embedVar.set_image(url=link)
        await message_channel.send(embed=embedVar)

    #send embed anime info
    async def embed_anime_info(self, ctx, info):
        studios = ''
        if info['studios'] != []:
            for i in range(0, len(info['studios'])):
                studios += f"[{info['studios'][i]['name']}]({info['studios'][i]['url']})\n"
        else:
            studios = 'N/A'
        embedVar = discord.Embed(title=f"**{info['title']}**", url=info['url'], description=f"**Type:** {info['type']}", color=int(self.cfg['anime_color'], 16))
        embedVar.add_field(name="⭐ Score:", value=info['score'])
        embedVar.add_field(name="Source:", value=info['source'])
        embedVar.add_field(name="Studio(s):", value=studios)
        embedVar.add_field(name="Season:", value=info['season'])
        embedVar.add_field(name="Start date:", value=info['start'])
        embedVar.add_field(name="End:", value=info['end'])
        embedVar.add_field(name="Synopsis:", value=info['synopsis'], inline=False)
        embedVar.set_thumbnail(url=info['image'])
        embedVar.set_author(name='ANIME')
        await ctx.send(embed=embedVar)
        
        if info['trailer'] != None:
            i = info['trailer'].find('?')
            info['trailer'] = info['trailer'][:i].replace("embed/", "watch?v=")
            await ctx.send(info['trailer'])

    #send embed manga info
    async def embed_manga_info(self, ctx, info):
        authors = ''
        if info['authors'] != []:
            for i in range(0, len(info['authors'])):
                authors += f"[{info['authors'][i]['name'].replace(',', '')}]({info['authors'][i]['url']})\n"
        else:
            authors = 'N/A'
        embedVar = discord.Embed(title=f"**{info['title']}**", url=info['url'], description=f"**Type:** {info['type']}", color=int(self.cfg['manga_color'], 16))
        embedVar.add_field(name="⭐ Score:", value=info['score'])
        embedVar.add_field(name="Author(s):", value=authors)
        embedVar.add_field(name="Status:", value=info['status'])
        embedVar.add_field(name="Start date:", value=info['start'])
        embedVar.add_field(name="End:", value=info['end'])
        embedVar.add_field(name="Synopsis:", value=info['synopsis'], inline=False)
        embedVar.set_thumbnail(url=info['image'])
        embedVar.set_author(name="MANGA")
        await ctx.send(embed=embedVar)

    #send embed character info
    async def embed_character(self, ctx, info):
        if info['alter_name'] != []:
            alternative_names = '**AKA:**'
            for i in range(0, len(info['alter_name'])):
                if len(alternative_names) <= 900:
                    alternative_names += f" {info['alter_name'][i]} |"
                else:
                    break
        else:
            alternative_names = ''
        
        if info['anime'] != []:
            animes = ''
            for i in range(0, len(info['anime'])):
                if len(animes) <= 900:
                    animes += f"[{info['anime'][i]['name']}]({info['anime'][i]['url']})\n"
                else:
                    break
        else:
            animes = 'N/A'
        
        if info['manga'] != []:
            mangas = ''
            for i in range(0, len(info['manga'])):
                if len(mangas) <= 900:
                    mangas += f"[{info['manga'][i]['name']}]({info['manga'][i]['url']})\n"
                else:
                    break
        else:
            mangas = 'N/A'

        embedVar = discord.Embed(title=info['name'], url=info['url'], description=alternative_names, color=int(self.cfg['anime_character_color'], 16))
        embedVar.add_field(name="Anime:", value=animes)
        embedVar.add_field(name="Manga:", value=mangas)
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

    #send embed anime character info
    async def embed_anime_characters_info(self, ctx, info):
        voice_actors_name = ''
        if info['voice'] != []:
            for i in range(0, len(info['voice'])):
                voice_actors_name += f"[{info['voice'][i]['name']}]({info['voice'][i]['url']})\n"
        else:
            voice_actors_name = 'N/A'
        embedVar = discord.Embed(title=info['name'], url=info['url'], color=int(self.cfg['anime_character_color'], 16))
        embedVar.add_field(name="Seiyuu:", value=voice_actors_name)
        embedVar.add_field(name="Role:", value=info['role'])
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

    #send embed manga character info
    async def embed_manga_characters_info(self, ctx, info):
        embedVar = discord.Embed(title=info['name'], url=info['url'], description=f"**Role:** {info['role']}", color=int(self.cfg['manga_character_color'], 16))
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)
        
    #send embed seiyuu info
    async def embed_seiyuu_info(self, ctx, info):
        embedVar = discord.Embed(title=info['name'], url=info['url'], color=int(self.cfg['seiyuu_color'], 16))
        embedVar.add_field(name="Voice:", value=f"[{info['character']}]({info['character_url']})")
        embedVar.add_field(name="Role:", value=info['role'])
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

    #send embed anime's staff info
    async def embed_anime_staff_info(self, ctx, info):
        positions = ''
        if info['positions'] != 'N/A':
            for i in range(0, len(info['positions'])):
                positions += f"{info['positions'][i]}\n"
        else:
            positions = 'N/A'
        embedVar = discord.Embed(title=info['name'], url=info['url'], color=int(self.cfg['staff_color'], 16))
        embedVar.add_field(name="Position(s):", value=positions)
        embedVar.set_thumbnail(url=info['image'])
        await ctx.send(embed=embedVar)

#================================================================================================================================================

    @commands.command(name='lewd', help='Send random NSFW waifu pic or gif')
    async def lewd(self, ctx, *, arg=''):
        if arg in self.cfg['hentai_categories']:
            link = self.get_waifu_pics('nsfw', arg)
        else:
            link = self.get_waifu_pics('nsfw', random.choice(self.cfg['hentai_categories']))

        if not link:
            await ctx.send("❌  **- Error**")
        else:
            channel_id = ctx.channel.id
            message_channel = self.bot.get_channel(channel_id)
            await self.embed_image(message_channel, link, int(self.cfg['hentai_color'], 16))

    @commands.command(name='waifu', help='Send random SFW waifu pic or gif')
    async def waifu(self, ctx, *, arg=''):
        if arg in self.cfg['waifu_categories']:
            link = self.get_waifu_pics('sfw', arg)
        else:
            link = self.get_waifu_pics('sfw', random.choice(self.cfg['waifu_categories']))

        if not link:
            await ctx.send("❌  **- Error**")
        else:
            channel_id = ctx.channel.id
            message_channel = self.bot.get_channel(channel_id)
            await self.embed_image(message_channel, link, int(self.cfg['waifu_color'], 16))
    
    @commands.command(name='aniquote', help='Send random anime quote', aliases=['aquote', 'aq'])
    async def aniquote(self, ctx):
        quote = self.get_anime_quote()
        if not quote:
            await ctx.send("❌  **- Error**")
        else:
            await ctx.send(quote)

    @commands.command(name='anime', help='Search for anime', aliases=['a', 'ani'])
    async def anime(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        self.info = self.search('anime', item)
        if not self.info:
            await ctx.send('❌  **- Try again later** ↻')
        else:
            await self.embed_anime_info(ctx, self.info)
        self.previous_command = 'anime'

    @commands.command(name='manga', help='Search for manga', aliases=['m'])
    async def manga(self, ctx, *items):
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")

        self.info = self.search('manga', item)
        if not self.info:
            await ctx.send('❌  **- Try again later** ↻')
        else:
            await self.embed_manga_info(ctx, self.info)
        self.previous_command = 'manga'
    
    @commands.command(name='character', help='Search for characters in anime', aliases=['char'])
    async def character(self, ctx, *, arg=''):
        #search character
        if arg != 'main' and arg != 'support' and arg != '':
            if self.search_character(arg) == False:
                await ctx.send('❌  **- Try again later** ↻')
                return
            for i in range(0, len(self.characters_staff)):
                await self.embed_character(ctx, self.characters_staff[i])
            return

        if self.previous_command != 'manga' and self.previous_command != 'anime':
            await ctx.send(f"❌  **- Use** `anime` **or** `manga` **before this command.**")
            return
            
        arg = self.convert_arg(arg)
        max_characters = self.cfg['characters_number']
        await ctx.send(f"🔎 **Searching**")

        if self.info['identify'] == 'manga':
            #search character in manga
            if self.get_manga_characters_info(arg) == False:
                await ctx.send('❌  **- Try again later** ↻')
                return
            else:
                if len(self.characters_staff) < max_characters:
                    max_characters = len(self.characters_staff)
                for i in range(0, max_characters):
                    await self.embed_manga_characters_info(ctx, self.characters_staff[i])

        else:
            #search character in anime
            if self.get_characters_staff_info('characters', arg) == False:
                await ctx.send('❌  **- Try again later** ↻')
                return
            else:
                if len(self.characters_staff) < max_characters:
                    max_characters = len(self.characters_staff)
                for i in range(0, max_characters):
                    await self.embed_anime_characters_info(ctx, self.characters_staff[i])

    @commands.command(name='staff', help="Search for anime's staff", aliases=['stf'])
    async def staff(self, ctx):
        if self.previous_command != 'anime':
            await ctx.send(f"❌  **- Use** `anime` **before this command.**")
            return

        max_characters = self.cfg['characters_number']
        await ctx.send(f"🔎 **Searching**")

        if self.get_characters_staff_info('staff', '') == False:
            await ctx.send('❌  **- Try again later** ↻')
            return
        else:
            if len(self.characters_staff) < max_characters:
                max_characters = len(self.characters_staff)
            for i in range(0, max_characters):
                await self.embed_anime_staff_info(ctx, self.characters_staff[i])

    @commands.command(name='seiyuu', help="Search for anime's seiyuu", aliases=['sei'])
    async def seiyuu(self, ctx, *, arg=''):
        if self.previous_command != 'anime':
            await ctx.send(f"❌  **- Use** `anime` **before this command**")
            return

        arg = self.convert_arg(arg)
        max_characters = self.cfg['characters_number']
        await ctx.send(f"🔎 **Searching**")

        
        if self.get_characters_staff_info('characters', arg) == False:
            await ctx.send('❌  **- Try again later** ↻')
            return

        else:
            if len(self.characters_staff) < max_characters:
                max_characters = len(self.characters_staff)
            
            for i in range(0, max_characters):
                for j in range(0, len(self.characters_staff[i]['voice'])):
                    temp = self.characters_staff[i]['voice'][j]
                    temp['character'] = self.characters_staff[i]['name']
                    temp['character_url'] = self.characters_staff[i]['url']
                    temp['character_id'] = self.characters_staff[i]['id']
                    temp['role'] = self.characters_staff[i]['role']
                    await self.embed_seiyuu_info(ctx, temp)

    @commands.command(name='nhentai', help="Search 'cultured' manga on 'nhentai'", aliases=['ntai'])
    async def nhentai(self, ctx, *items):
        item = ' '.join(items)
        if item.isdigit:
            if not Hentai.exists(item):
                await ctx.send(f"❌ `{item}` **does not exist.**")
                return

            doujin = Hentai(item)
            tags = ''
            for tag in doujin.tag:
                tags += f"`{tag.name}`  "

            relateds = ''
            for related in doujin.related:
                if len(relateds) <= 900:
                    relateds += f"[`{related.id}`]({related.url})  "
                else:
                    break

            characters = ''
            for character in doujin.character:
                characters += f"[`{character.name.title()}`]({character.url})  "
            
            languages = ''
            for language in doujin.language:
                languages += f"{language.name.capitalize()} "

            embedVar = discord.Embed(title=doujin.title(Format.Pretty), url=f"https://nhentai.net/g/{item}", description=f"**ID:** {item}", color=0xec2854)
            embedVar.add_field(name="Artist:", value=f"[{Tag.get(doujin.artist, property_='name').title()}]({Tag.get(doujin.artist, property_='url')})")
            if doujin.parody != []:
                embedVar.add_field(name="Parody:", value=f"[{Tag.get(doujin.parody, property_='name').title()}]({Tag.get(doujin.parody, property_='url')})")
            embedVar.add_field(name="Language:", value=languages)
            if doujin.character != []:
                embedVar.add_field(name="Characters:", value=characters, inline=False)
            if doujin.tag != []:
                embedVar.add_field(name="Tags:", value=tags, inline=False)
            if doujin.related != []:
                embedVar.add_field(name="Related:", value=relateds, inline=False)
            embedVar.set_thumbnail(url=doujin.cover)
            await ctx.send(embed=embedVar)
    
    @commands.command(name='set_lewd', help='Set message channel to send lewd.')
    async def set_lewd(self, ctx, time):
        background_lewd = {
            'channel': ctx.channel.id,
            'time': time
        }
        with open("config.json", 'r') as file:
            data = json.load(file)
            file.close()

        data['ANIME']['background_lewd'] = background_lewd.copy()
        self.cfg['background_lewd'] = background_lewd.copy()

        with open("config.json", 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.close()
        await ctx.send("✅ **Done!**")

    @commands.command(name='set_lewd_off', help='Turn off lewd channel.')
    async def set_lewd_off(self, ctx):
        with open("config.json", 'r') as file:
            data = json.load(file)
            file.close()

        data['ANIME']['background_lewd'] = {}
        self.cfg['background_lewd'] = {}

        with open("config.json", 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.close()
        await ctx.send("📴 **Turned off lewd channel.**")

    @tasks.loop(seconds=60)
    async def background_lewd(self):
        if self.cfg['background_lewd'] != {}:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            time = self.cfg['background_lewd']['time']

            if current_time == time:
                link = self.get_waifu_pics('nsfw', random.choice(self.cfg['hentai_categories']))
                channel_id = self.cfg['background_lewd']['channel']
                message_channel = self.bot.get_channel(channel_id)
                await self.embed_image(message_channel, link, int(self.cfg['hentai_color'], 16))

    @background_lewd.before_loop
    async def check(self):
        await self.bot.wait_until_ready()
