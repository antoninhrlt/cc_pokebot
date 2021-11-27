#!/bin/python3

import discord
import asyncio
import music
from token import token

client = discord.Client()

bot_channel_id = 914086774287007765

BAN_WORDS = ["pokeball", "carapuce", "dresseurs", "javascript", "giratina"]

async def send(what, title=None):
    channel = client.get_channel(bot_channel_id)
    if title != None:
        embed = discord.Embed(title=title, description=what)
    else:
        embed = discord.Embed(description=what)
    await channel.send(embed=embed)

async def delete_message(message):
    await message.delete()

async def check_banned_messages(message):
    for ban_word in BAN_WORDS:
        if ban_word in message.content:
            copy = message.content
            author = message.author

            await delete_message(message)
            await send("Your message was deleted, don't start again !\n" 
                + f"Message sent: **{copy}**; by **{author}**",
                title="WHO WHO WHO, you can't say that !")
            break

async def play(message):
    url = message.content.split(' ')[1]
    music_client = music.Music(client)
    await music_client.play(message, url)

@client.event
async def on_ready():
    await send("i'm alive !")
    print("> bot started")

@client.event
async def on_message(message):
    if message.channel.id == bot_channel_id: # works only in "pokebot-anto"
        await check_banned_messages(message)

        if message.content == "$hello":
            await send("hi !")

        if "$play" in message.content:
            await play(message)

print("> starting bot ...")
client.run(token)