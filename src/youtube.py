from youtube_dl import YoutubeDL
import discord
import youtube_dl
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
youtube_dl.utils.bug_reports_message = lambda: ''
ffmpeg_options = {
    'before_options': " -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
clients = {}  # {guild: MusicClient, ...}

async def get_client(message, client):
    global clients
    if not str(message.guild.id) in clients:
        clients[str(message.guild.id)] = await MusicClient.create(message, client)
    return clients[str(message.guild.id)]

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, option=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **option), data=data)


class Youtube:
    def __init__(self, url):
        dl = YoutubeDL({'format': 'bestaudio'})
        dl.extract_info(url)
