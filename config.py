#admin
prefix="?"

#music options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {
    'format': 'bestaudio[ext=m4a]',
    'noplaylist': 'True'
}

queued_music = {
    'header': "▷ **Queue:**",
    'color': 0xe67e22,
    'info1': "Position in queue"
}

playing_music = {
    'header': "🎵  **Playing:**",
    'color': 0xff0000,
    'info1': "Songs in queue"
}

max_songs_in_queue = 10
disconnect_time = 1800

#anime function options
hentai_color = 0xd59de0
waifu_color = 0x2e51a2

anime_color = 0x2e51a2
manga_color = 0xebab37
character_color = 0x2e51a2
seiyuu_color = 0x2e51a2
staff_color = 0x2e51a2

characters_number = 10
language = "Japanese"