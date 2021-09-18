import discord
from discord.ext import commands
from youtube_dl.YoutubeDL import YoutubeDL
import asyncio
import time

import config

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False

        self.music_queue = []
        self.voice_channel = ""
        self.message_channel = ""
        self.current_song = ""

    #search youtube for item
    def yt_search(self, query):
        with YoutubeDL(config.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f'ytsearch:{query}', download=False)['entries'][0]
            except Exception:
                return False
            
            return {'source': info['formats'][0]['url'], 'title': info['title'], 'channel': info['channel'],
                    'duration': info['duration'], 'web': info['webpage_url'], 'thumbnail': info['thumbnail']}
    
    #convert second to h:m:s format
    def second_convert(self, duration):
            m, s = divmod(duration, 60)
            h, m = divmod(m, 60)

            if s < 10:
                second = f"0{s}"
            else:
                second = s

            if h != 0:
                if  m < 10:
                    minute = f"0{m}"
                else:
                    minute = m
                return f"{h}:{minute}:{second}"
            else:
                return f"{m}:{second}"

    #display song's info
    async def song_info(self, info, config, songs_number):
        embedVar = discord.Embed(title=config['header'], description=f"**[{info['title']}]({info['web']})**", color=config['color'])
        embedVar.add_field(name="Channel:", value=info['channel'], inline=True)
        embedVar.add_field(name="Duration:", value=self.second_convert(info['duration']))
        
        if songs_number == 0:
            embedVar.add_field(name=config['info3'], value=len(self.music_queue))
        else:
            embedVar.add_field(name=config['info3'], value=songs_number)
        
        embedVar.set_thumbnail(url= info['thumbnail'])
        embedVar.set_footer(icon_url= info['avatar'], text= f"Added by {info['author']}")
        await self.message_channel.send(embed=embedVar)  

    #auto disconnect when not playing
    async def auto_disconnect(self, ctx):
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(config.disconnect_time)
            while ctx.voice_client.is_playing():
                break
            else:
                await ctx.voice_client.disconnect()

    #play next song in queue
    async def play_next(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            info = self.music_queue[0]
            self.music_queue.pop(0)
            
            url = info['source']
            source = discord.FFmpegOpusAudio(url, **config.FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda e : self.my_after(ctx))
            
            self.current_song = f"[{info['title']}]({info['web']}) | `{self.second_convert(info['duration'])}`"
            await self.song_info(info, config.playing_music, 0)
            print(f"PLAYING: '{info['title']}'")
            await self.auto_disconnect(ctx)
        
        else:
            self.is_playing = False
    
    #to pass it into the fucking "lambda e" in "play_next" function
    def my_after(self, ctx):
        coro = self.play_next(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass
    
    #check if someone try to outsmart the bot
    async def check_voice_channel(self, ctx):
        self.message_channel = ctx.channel
        #check if the message's sender is in a voice channel
        if ctx.author.voice is None:
            await ctx.send(f'❌ **- Get in the voice channel, **`{str(ctx.message.author)[:-5]}`')
            return False

        #check if the bot is in any voice channel
        if ctx.voice_client is None:
            await ctx.send('❌ **- Cannot use this command right now**')
            return False

        #check if the bot had already connected to the right voice chat
        if ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send('❌ **- You need to get in the same voice channel as me**')
            return False

        return True

#================================================================================================================================================

    @commands.command(name='play', help='Play audio from Youtube', aliases=['p'])
    async def play(self, ctx, *items):

        self.message_channel = ctx.channel

        #check if the message's sender is in a voice channel
        if ctx.author.voice is None:
            await ctx.send(f'❌ **- Get in the voice channel, **`{str(ctx.message.author)[:-5]}`')
            return

        #check if the bot is in any voice channel
        if ctx.voice_client is None:
            self.voice_channel = await ctx.author.voice.channel.connect()
            await ctx.send(f'⤵ **Joined **`{ctx.author.voice.channel}`')

        #check if command sender had already connected to the bot's voice channel
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send('❌ **- You need to get in the same voice channel as me**')
            return

        #jump to song in queue
        item = " ".join(items)
        if item.isdigit():
            await self.jump(ctx, item)
            return

        #Get video link from Youtube then stream
        await ctx.send(f"🔎 **Searching** `{item}`")
        info = self.yt_search(item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
            return
        
        info['avatar'] = ctx.author.avatar_url
        info['author'] = ctx.author.name
        self.music_queue.append(info)
        await ctx.send(f"**▷** ***Queued*** **:**  `{info['title']}`")

        if not self.is_playing:
            await self.play_next(ctx)

    @commands.command(name='join', help='Join a voice channel')
    async def join(self, ctx):
        self.message_channel = ctx.channel

        #check if the message's sender is in a voice channel
        if ctx.author.voice is None:
            await ctx.send(f'❌ **- Get in the voice channel, **`{str(ctx.message.author)[:-5]}`')
            return

        #check if the bot is in any voice channel
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            self.voice_channel = await voice_channel.connect()
            await ctx.send(f'⤵ **Joined **`{voice_channel}`')
            await self.auto_disconnect(ctx)
            return

        #check if the bot had already connected to the right voice channel
        if voice_channel == ctx.voice_client.channel:
            await ctx.send(f'❌ **- Already join **`{voice_channel}`')

        else:
            ctx.voice_client.pause()
            await ctx.voice_client.move_to(voice_channel)
            await ctx.send(f'➡ **Moved to **`{voice_channel}`')
            ctx.voice_client.resume()
        await self.auto_disconnect(ctx)

    @commands.command(name='leave', help='Leave voice chat', aliases=['disconnect'])
    async def leave(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        voice_chat = ctx.voice_client
        if voice_chat.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.send('👋 **Bye bye!**')

        else:
            await ctx.send('❌**- Already disconnected**')

    @commands.command(name='pause', help='Pause music')
    async def pause(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('⏸ ***Paused***')

        else:
            await ctx.send('❌ **- Already paused**')
        
    @commands.command(name='resume', help='Resume music')
    async def resume(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('⏯ ***Resuming***')

        else:
            await ctx.send('❌ **- Already playing**')

    @commands.command(name='skip', help='Skip current music', aliases=['next'])
    async def skip(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        if self.voice_channel:
            ctx.voice_client.stop()
            await ctx.send('⏭ ***Skipped***')

    @commands.command(name="queue", help="Display current songs in queue", aliases=['q'])
    async def queue(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        songs = ""
        total_duration = 0
        in_queue = False
        max_songs_in_queue = config.max_songs_in_queue
        songs_number = len(self.music_queue)

        #max songs that I can create in queue list is around 12 or lower
        for i in range(0, songs_number):
            if i < max_songs_in_queue:
                songs += f"`{i+1}.` {self.music_queue[i]['title']} | `{self.second_convert(self.music_queue[i]['duration'])}`\n\n"
                in_queue = True
            total_duration += self.music_queue[i]['duration']

        if songs_number <= max_songs_in_queue:
            songs += f"**{songs_number} songs in queue | {self.second_convert(total_duration)} total length**"
        else:
            songs += f"{songs_number - max_songs_in_queue} more song(s)\n**{songs_number} songs in queue | {self.second_convert(total_duration)} total length**"

        if in_queue:
            embedVar = discord.Embed(title="▷ **QUEUE:**", color=0x83f8c9)
            embedVar.add_field(name="__Now Playing:__", value=self.current_song, inline=False)
            embedVar.add_field(name="__Next:__", value=songs ,inline=False)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(f"⛔ **No music in queue**")

    @commands.command(name='clear', help='Clear ALL musics in queue', aliases=['clr'])
    async def clear(self, ctx):
        if not await self.check_voice_channel(ctx):
            return

        if len(self.music_queue) != 0:
            self.music_queue.clear()
            await ctx.send('💥 ***Cleared All***')
        else:
            await ctx.send("❌ **- Nothing to clear**")

    @commands.command(name='remove', help='Remove ONE music in queue', aliases=['rm'])
    async def remove(self, ctx, item):
        if not await self.check_voice_channel(ctx):
            return

        number = int(item) - 1
        if number < 0:
            await ctx.send("❌ **- You are the fucking reason I had to foolproof this command**")
            return

        if len(self.music_queue) != 0:
            if number < len(self.music_queue):
                await ctx.send(f"🧹 ***Removed*** `{self.music_queue[number]['title']}`")
                self.music_queue.pop(number)
            else:
                await ctx.send("❌ **- That song don't exist**")
        else:
            await ctx.send("❌ **- Nothing to remove**")

    #@commands.command(name='jump', help='Jump to music in queue')
    async def jump(self, ctx, item):
        if not await self.check_voice_channel(ctx):
            return

        number = int(item) - 1
        if number < 0:
            await ctx.send("❌ **- You are the fucking reason I had to foolproof this command**")
            return

        if number == 0:
            await ctx.send("**Yes, you can do this but why though**❔\n⏭ ***Skipped***")
            ctx.voice_client.stop()
            return
        
        if len(self.music_queue) != 0:
            if number < len(self.music_queue):
                await ctx.send(f"**↷** ***Jump to*** `{self.music_queue[number]['title']}`")
                self.music_queue = self.music_queue[number:]
                ctx.voice_client.stop()
            else:
                await ctx.send("❌ **- That song don't exist**")
        else:
            await ctx.send("❌ **- Nothing to jump to**")
    
    @commands.command(name='info', help='Display info of music in queue')
    async def info(self, ctx, item):
        if not await self.check_voice_channel(ctx):
            return

        number = int(item) - 1
        if number < 0:
            await ctx.send("❌ **- You are the fucking reason I had to foolproof this command**")
            return
        
        if len(self.music_queue) != 0:
            if number <= len(self.music_queue):
                await self.song_info(self.music_queue[number], config.queued_music, number + 1)
        
            else:
                await ctx.send("❌ **- That song don't exist**")
        else:
            await ctx.send("❌ **- Nothing to show**")

    @commands.command(name='rickroll', help='Tag a person to rickroll', aliases=['rick'])
    async def rickroll(self, ctx):

        #this part gave me too much headache so i foolproofed it
        try:
            acc = ctx.message.mentions[0]
        except:
            return

        #check if they try to make the bot rickroll itself
        name = str(acc)
        await ctx.send(f"**OPERATION:  **`Rickroll {name[:-5]}`")
        if name == str(self.bot.user):
            await ctx.send("**Ha ha! Do you think I'm that stupid  😎**")
            return

        #check if tagged person is a bot
        if acc.bot:
            await ctx.send("**LMAO, that's a bot**  🙂")
            return

        #check if that person is in a voice chat
        if acc.voice is None:
            await ctx.send(f"❌ **Operation Failed** ❌")
            return

        voice_channel = acc.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()

        #check if the bot had already connected to the right voice chat
        elif voice_channel == ctx.voice_client.channel:
            ctx.voice_client.stop()
        else:
            await ctx.voice_client.disconnect()
            await voice_channel.connect()

        voice_chat = ctx.voice_client
        voice_chat.play(discord.FFmpegPCMAudio(source="data/Rickroll.mp3"))
        await ctx.send(f"😆🎤  **Successfully rickrolled **`{name[:-5]}`")
        time.sleep(18)
        await voice_chat.disconnect()

def setup(bot):
    bot.add_cog(music(bot))