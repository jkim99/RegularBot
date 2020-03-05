#!/bin/bash
"""
regular.py
it's anything bot
"""

from datetime import datetime
from regular.reddit import REDDIT
from regular.youtube import YOUTUBE
from regular.creds import BOT_TOKEN
from regular.creds import CLASH_API_KEY
from discord.ext import commands
from discord.utils import get
# from discord import opus
from discord import File
from discord import FFmpegPCMAudio as audio
import asyncio
import regular.config as config
import os
import random
import requests


client = commands.Bot(command_prefix=config.PREFIX)
reddit = REDDIT()
youtube = YOUTUBE()


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
    await ctx.send(f"{ctx.author.display_name} rolls a {str(result)}")


@client.command(pass_context=True)
async def shutdown(ctx):
    log(ctx.message.content, ctx.message.author)
    youtube.clear_mp3()
    await ctx.send('Stopping...')
    await client.logout()


@client.command(pass_context=True, aliases=['suggest', 'suggestions', 'sug'])
async def suggestion(ctx):
    log(ctx.message.content, ctx.message.author)

    cmd = ctx.message.content.split()[0].replace(config.PREFIX, "")

    t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
    file = open('suggestions.txt', 'a')
    content = ctx.message.content.replace(config.PREFIX + cmd, '')
    file.write('\n{}{} [{}]'.format(t, content, str(ctx.message.author)))
    file.close()
    await ctx.send('Thank you for the suggestion!')


@client.command(pass_context=True, aliases=['lq'])
async def listqueue(ctx):
    await ctx.send(youtube.print_queue())

@client.command(pass_context=True)
async def meme(ctx, subreddit='dankmemes'):
    log(ctx.message.content, ctx.message.author)
    filename = reddit.get_meme()
    while filename == '':
        filename = reddit.get_meme()
    await ctx.send(file=File(filename))
    os.remove(filename)


@client.command(pass_context=True, aliases=['play', 'que', 'q'])
async def queue(ctx, url=None):
    log(ctx.message.content, ctx.message.author)

    # joining channel
    try:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You must be connected to a voice channel")
            return
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except AttributeError:
        await ctx.send("You must be connected to a voice channel")
        return

    # downloads and queues song if url exists
    if url:
        youtube.queue_song(url)
    else:
        await ctx.send(f"Usage: {config.PREFIX}play [youtube url]")
        return

    # plays the song
    song = youtube.pop_queue()
    voice.play(audio(song))
    await ctx.send(f"Playing: {song}")


@client.command(pass_context=True)
async def skip(ctx):
    log(ctx.message.content, ctx.message.author)
    voice.stop()
    await ctx.send("Skipping...")
    song = youtube.pop_queue()
    await ctx.send(f"Playing: {song}")
    voice.play(audio(song))
    

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
    headers = {'Accept': 'application/json',
               'authorization': 'Bearer {}'.format(CLASH_API_KEY)}
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


@client.command(pass_context=True)
async def stop(ctx):
    log(ctx.message.content, ctx.message.author)
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()


def main():
    # if not opus.is_loaded():
    #     opus.load_opus('opus')
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
