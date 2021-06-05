"""
modules.py
it's anything bot
"""

from datetime import datetime
from modules.reddit import REDDIT
from modules.youtube import YOUTUBE
from discord.ext import commands
from discord.utils import get
from discord import File
from discord import FFmpegPCMAudio
import os
import sys
import random
import yaml

# Load config from input file
if ".yaml" not in sys.argv[1] and ".yml" not in sys.argv[1]:
    print("Config file must be .yml or .yaml")
    sys.exit()

with open(sys.argv[1]) as config_file:
    config = yaml.load(config_file)

client = commands.Bot(command_prefix=config.get("command_prefix"))

reddit = REDDIT()
youtube = YOUTUBE()


def log(message, author):
    t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
    with open('log.txt', 'a') as logfile:
        logfile.write('\n{} {} [{}]'.format(t, str(message), str(author)))


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
        youtube.enqueue(url)
    else:
        await ctx.send(f"Usage: `{config.PREFIX}play [youtube url]`")
        return

    # plays the song
    song = youtube.pop_queue()
    voice.play(FFmpegPCMAudio(song))
    await ctx.send(f"Playing: {song}")


@client.command(pass_context=True)
async def skip(ctx):
    log(ctx.message.content, ctx.message.author)
    await ctx.send("This command is currently unavailable")
    # voice.stop()
    # await ctx.send("Skipping...")
    # song = youtube.pop_queue()
    # await ctx.send(f"Playing: {song}")
    # voice.play(FFmpegPCMAudio(song))


@client.command(pass_context=True)
async def stop(ctx):
    log(ctx.message.content, ctx.message.author)
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()


def main():
    bot_token = config.get("discord").get("bot_token")
    client.run(bot_token)


if __name__ == '__main__':
    main()
