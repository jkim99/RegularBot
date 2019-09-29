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
# temp
import discord
import os


PREFIX = '.'
client = commands.Bot(command_prefix=PREFIX)
reddit = REDDIT()


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


@client.command(pass_context=True)
async def meme(ctx):
    log(ctx.message.content, ctx.message.author)
    filename = reddit.get_meme()
    if filename < 0:
        return
    await ctx.send(file=File(filename))
    os.remove(filename)


# TODO: fix this shit
@client.command(pass_context=True)
async def play(ctx, url):
    log(ctx.message.content, ctx.message.author)
    voice = ctx.message.author.voice
    if voice:
        channel = voice.channel
        voice_client = await channel.connect()
        # voice_client.play(a, after=None)


def main():
    if not opus.is_loaded():
        opus.load_opus('opus')
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
