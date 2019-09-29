"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
from creds import BOT_TOKEN
from discord.ext import commands
from discord import opus
from discord import File
from discord import FFmpegPCMAudio as audio
import os
import youtube_dl


PREFIX = '.'
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
