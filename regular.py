"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
from youtube import YOUTUBE
from creds import BOT_TOKEN
from discord.ext import commands
from discord.utils import get
from discord import opus
from discord import File
from discord import FFmpegPCMAudio as audio
import os


PREFIX = '&'  # for the beta bot
client = commands.Bot(command_prefix=PREFIX)
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
    await ctx.send(file=File(filename))
    os.remove(filename)


@client.command(pass_context=True)
async def play(ctx, url=None):
    log(ctx.message.content, ctx.message.author)

    # joining channel
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You must be connected to a voice channel")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    # queues url if it exists
    if url:
        youtube.queue_song(url)

    # downloads and plays the song
    voice.play(audio(youtube.download()))
    voice.volume = 100
    voice.is_playing()


@client.command(pass_context=True, aliases=['que', 'q'])
async def queue(ctx, url):
    log(ctx.message.content, ctx.message.author)
    youtube.queue_song(url)


@client.command(pass_context=True)
async def stop(ctx):
    log(ctx.message.content, ctx.message.author)
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()


def main():
    if not opus.is_loaded():
        opus.load_opus('opus')
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
