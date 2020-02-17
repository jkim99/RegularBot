#!/bin/bash
"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
from creds import BOT_TOKEN
from creds import CLASH_API_KEY
from discord.ext import commands
from discord import opus
from discord import File
from discord import FFmpegPCMAudio as audio
import os
import youtube_dl
import random
import threading
import requests


PREFIX = '_'
client = commands.Bot(command_prefix=PREFIX)
reddit = REDDIT()
youtube_queue = []


def log(message, author):
    t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
    file = open('log.txt', 'a')
    file.write('\n{} {} [{}]'.format(t, str(message), str(author)))
    file.close()


@client.event
async def on_ready():
    print('Bot is ready!')


@client.command(pass_context=True)
async def ping(ctx):
    log(ctx.message.content, ctx.message.author)
    await ctx.send('pong!')


@client.command(pass_context=True)
async def roll(ctx):
    log(ctx.message.content, ctx.message.author)
    result = int(random.random() * 100)
    await ctx.send('Rolling out of 100...')
    await ctx.send(ctx.author.display_name + ' rolls a ' + str(result))


@client.command(pass_context=True)
async def shutdown(ctx):
    log(ctx.message.content, ctx.message.author)
    await ctx.send('Stopping...')
    await client.logout()


@client.command(pass_context=True, aliases=['suggest', 'suggestions', 'sug'])
async def suggestion(ctx):
    log(ctx.message.content, ctx.message.author)
    t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
    file = open('suggestions.txt', 'a')
    content = ctx.message.content.replace(PREFIX + 'suggestion', '')
    file.write('\n{}{} [{}]'.format(t, content, str(ctx.message.author)))
    file.close()
    await ctx.send('Thank you for the suggestion!')


@client.command(pass_context=True)
async def meme(ctx):
    log(ctx.message.content, ctx.message.author)
    filename = reddit.get_meme()
    while filename == '':
        filename = reddit.get_meme()
    await ctx.send(file=File(filename))
    os.remove(filename)


@client.command(pass_context=True)
async def play(ctx):
    log(ctx.message.content, ctx.message.author)
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    while True:
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
            else:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_queue[0]])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                voice.play(audio("song.mp3"))
                voice.volume = 100
                voice.is_playing()
                youtube_queue.pop()
        except PermissionError:
            pass


@client.command(pass_context=True, aliases=['members'])
async def clanmembers(ctx):
    log(ctx.message.content, ctx.message.author)
    headers = {
        'Accept': 'application/json',
        'authorization': 'Bearer {}'.format(CLASH_API_KEY)
    }
    response = requests.get(
        'https://api.clashofclans.com/v1/clans/%232PCQRQVY/members',
        headers=headers
    )
    if 200 <= response.status_code <= 299:
        r_json = response.json()
        message = '\n ::: Clan members :::\n'
        for member in r_json['items']:
            message += 'Name: {}, Trophies: {}, Donation ratio: {}\n'.format(
                        member['name'],
                        member['trophies'],
                        member['donations'] / member['donationsReceived']
            )
        await ctx.send(message)
    else:
        await ctx.send('Response error')


@client.command(pass_context=True, aliases=['war'])
async def clanwar(ctx):
    log(ctx.message.content, ctx.message.author)
    headers = {
        'Accept': 'application/json',
        'authorization': 'Bearer {}'.format(CLASH_API_KEY)
    }
    response = requests.get(
        'https://api.clashofclans.com/v1/clans/%232PCQRQVY/currentwar',
        headers=headers
    )
    if 200 <= response.status_code <= 299:
        r_json = response.json()
        if r_json['state'] == 'inWar':
            await ctx.send(
                'War is live! {} - {} VS {} - {}'.format(
                    r_json['clan']['name'],
                    r_json['clan']['stars'],
                    r_json['opponent']['name'],
                    r_json['opponent']['stars']
                ))
        else:
            await ctx.send('There is no war taking place right now.')
    else:
        await ctx.send('Response error')


@client.command(pass_context=True, aliases=['que', 'q'])
async def queue(ctx, url):
    log(ctx.message.content, ctx.message.author)
    youtube_queue.append(url)


@client.command(pass_context=True)
async def stop(ctx):
    log(ctx.message.content, ctx.message.author)


def main():
    if not opus.is_loaded():
        opus.load_opus('opus')
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
