from youtube import *
import discord

class Music:
    def __init__(self, client):
        self.client = client
    
    async def play(self, message, url):
        self.message = message
        if message.author.voice.channel:
            self.voice_client = await message.author.voice.channel.connect()
        else:
            raise RuntimeError("Not connected to a voice channel")
        
        player = await YTDLSource.from_url(url, loop=self.client.loop, 
            stream=True, option=ffmpeg_options)
   
        self.voice_client.play(player)

    async def disconnect(self):
        await self.message.author.voice.channel.disconnect()
