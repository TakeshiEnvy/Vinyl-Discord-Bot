import discord
from discord.ext import commands
from discord.player import FFmpegPCMAudio
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
import time
import asyncio

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format':'bestaudio[ext=m4a]', 'noplaylist':'True'}

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False

        self.music_queue = []
        self.voice_channel = ""
        self.current_song = ""
        self.previous_song = ""
        self.numbering = 0

    #search youtube for item
    def yt_search(self, item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f'ytsearch:{item}', download=False)['entries'][0]
                self.numbering += 1
            except Exception:
                return False
            return {'source': info['formats'][0]['url'], 'title': info['title'], 'number': self.numbering, 'channel': info['channel'], 'duration': info['duration']}

    #play next song in queue
    async def play_next(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            info = self.music_queue[0]
            self.current_song = f"{info['number']}) {info['channel']} - {info['title']}" 

            self.music_queue.pop(0)
            
            video_title = info['title']
            url = info['source']
            
            source = discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS)
            self.voice_channel.play(source, after=lambda e : self.my_after(ctx))

            await ctx.send(f"▶ **Playing **`{video_title}`")
            print(f"PLAYING: '{video_title}'")

        else:
            self.is_playing = False
    
    #to pass it into the fucking "lambda e" in "play_next" function
    def my_after(self, ctx):
        self.previous_song = self.current_song
        coro = self.play_next(ctx)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass
    
    @commands.command(name='play', help='Play audio drom Youtube', aliases=['p'])
    async def play(self, ctx, *items):

        #check if the message's sender is in a voice chat
        if ctx.author.voice is None:
            await ctx.send(f'❌  **Get in the fucking voice chat, **`{ctx.message.author}`')
            return

        #check if the bot is in any voice chat
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            self.voice_channel = await voice_channel.connect()
            await ctx.send(f'⤵ **Joined **`{voice_channel}`')

        else:
            #check if the bot had already connected to the right voice chat
            if voice_channel != ctx.voice_client.channel:
                await ctx.send('❌ **- You need to get in the same voice chat as me**')
                return

        #Get video link from Youtube then stream
        item = " ".join(items)
        await ctx.send(f"🔎 **Searching** `{item}`")
        info = self.yt_search(item)
        if not info:
            await ctx.send(f'❌ **- Not found** `{item}`')
            return
        self.music_queue.append(info)
        await ctx.send(f"**->** ***Queued*** **:**  `{info['title']}`")

        if not self.is_playing:
            await self.play_next(ctx)
    
    @commands.command(name='join', help='Join a voice channel')
    async def join(self, ctx):

        #check if the message's sender is in a voice chat
        if ctx.author.voice is None:
            await ctx.send(f'❌ **- Get in the fucking voice chat, **`{ctx.message.author}`')

        else:
            #check if the bot is in any voice chat
            voice_channel = ctx.author.voice.channel

            if ctx.voice_client is None:
                self.voice_channel = await voice_channel.connect()
                await ctx.send(f'⤵ **Joined **`{voice_channel}`')

            else:
                #check if the bot had already connected to the right voice chat
                if voice_channel == ctx.voice_client.channel:
                    await ctx.send(f'❌ **- Already join **`{voice_channel}`')

                else:
                    ctx.voice_client.pause()
                    await ctx.voice_client.move_to(voice_channel)
                    await ctx.send(f'➡ **Moved to **`{voice_channel}`')
                    ctx.voice_client.resume()

    @commands.command(name='leave', help='Leave voice chat', aliases=['disconnect'])
    async def leave(self, ctx):

        voice_chat = ctx.voice_client
        if voice_chat.is_connected():
            await ctx.voice_client.disconnect()
            await ctx.send('👋 **Bye bye!**')

        else:
            await ctx.send('❌**- Already disconnected**')

    @commands.command(name="queue", help="Displays the current songs in queue", aliases=['q'])
    async def queue(self, ctx):
        songs = ""
        songs_number = len(self.music_queue)
        if songs_number - 8 < 1:
            for i in range(0, songs_number):
                songs += str(self.music_queue[i]['number']) + ") " + self.music_queue[i]['channel'] + " - " + self.music_queue[i]['title'] + "\n"
            songs += "\n    This is the end of the queue!"

        else:
            for i in range(0, 8):
                songs += str(self.music_queue[i]['number']) + ") " + self.music_queue[i]['channel'] + " - " + self.music_queue[i]['title'] + "\n"
            songs += "\n    " + str(songs_number - 8) + " more song(s)"

        if not songs:
            await ctx.send("No music in queue")
        else:
            await ctx.send(f"```ml\n{self.previous_song}\n     ⬐ current track\n{self.current_song}\n     ⬑ current track\n{songs}```")

    @commands.command(name='pause', help='Pause music')
    async def pause(self, ctx):

        voice_chat = ctx.voice_client
        if voice_chat.is_playing():
            voice_chat.pause()
            await ctx.send('⏸ ***Paused***')

        else:
            await ctx.send('❌ **- Already paused**')
        
    @commands.command(name='resume', help='Resume music')
    async def resume(self, ctx):

        voice_chat = ctx.voice_client
        if voice_chat.is_paused():
            voice_chat.resume()
            await ctx.send('⏯ ***Resuming***')

        else:
            await ctx.send('❌ **- Already playing**')

    @commands.command(name='skip', help='Skip current music')
    async def skip(self, ctx):
        if self.voice_channel:
            ctx.voice_client.stop()
            await ctx.send('⏹ ***Skipped***')

    @commands.command(name='rickroll', help='Tag a person to rickroll', aliases=['rick'])
    async def rickroll(self, ctx):

        #this part gave me too much headache so i foolproofed it
        try:
            acc = ctx.message.mentions[0]
        except:
            return

        #check if they try to make the bot rickroll itself
        name = f"{acc}"
        await ctx.send(f"**OPERATION:  **`Rickroll {name}`")
        if name == 'Vinyl#5573':
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

        else:
            #check if the bot had already connected to the right voice chat
            if voice_channel == ctx.voice_client.channel:
                ctx.voice_client.stop()

            else:
                await ctx.voice_client.disconnect()
                await voice_channel.connect()

        voice_chat = ctx.voice_client

        voice_chat.play(discord.FFmpegPCMAudio(source='/home/pi/Appdata/VinylBot/data/Rickroll.mp3'))
        await ctx.send(f"😆🎤  **Successfully rickrolled **`{name}`")
        time.sleep(18)
        await voice_chat.disconnect()

def setup(bot):
    bot.add_cog(music(bot))