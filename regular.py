"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
# from spotify import SPOTIFY
from creds import BOT_TOKEN
from discord.ext import commands
from discord import opus
from discord import File
import os


PREFIX = '.'
client = commands.Bot(command_prefix=PREFIX)
reddit = REDDIT()


def log(message, author):
    print(message)
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
async def stop(ctx):
    log(ctx.message.content, ctx.message.author)
    await ctx.send('Stopping...')
    await client.logout()


@client.command(pass_context=True)
async def suggestion(ctx):
    log(ctx.message.content, ctx.message.author)
    t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
    file = open('suggestions.txt', 'a')
    content = ctx.message.content.replace(PREFIX + 'suggestion', '')
    file.write('\n{}{} [{}]'.format(t, content, str(ctx.message.author)))
    file.close()
    await ctx.send('Thank you for the suggestion!')


# TODO: fix this shit
@client.command(pass_context=True)
async def meme(ctx):
    filename = reddit.get_meme()
    await ctx.send(file=File(filename))
    os.remove(filename)


# TODO: fix this shit too
@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.channel
    voice_client = await channel.connect()
    player = await voice_client.create_ytdl_player(url)
    player.start()


def main():
    # opus.load_opus('opus')
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
