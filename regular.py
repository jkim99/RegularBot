"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
from spotify import SPOTIFY
import discord
# import random

BOT_TOKEN = 'NjI2OTM2ODY4MzM1Nzc5ODY1.XY1xig.klUPz5__kSkqWxHAoFWs_8KnjKo'
PREFIX = '!'
reddit = REDDIT()


class MyClient(discord.Client):
    visited_posts = []

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # this line right here gets the time
        t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')

        # this adds the message to the log
        log = open('log.txt', 'a')
        log.write('{}{} {}'.format(t, message.content, str(message.author)))
        log.close()

        # Ping --> Pong
        if message.content.startswith(PREFIX + 'ping'):
            await message.channel.send('pong!')

        # Takes suggestions and writes it to a file
        if message.content.startswith(PREFIX + 'suggestions'):
            file = open('suggestions.txt', 'a')
            content = message.content.replace(PREFIX + 'suggestions', '')
            file.write('\n{}{} [{}]'.format(t, content, str(message.author)))
            file.close()
            await message.channel.send('Thank you for the suggestion')

        # Invokes meme from the reddit module
        if message.content.startswith(PREFIX + 'meme'):
            reddit.command(message.content)


client = MyClient()
client.run(BOT_TOKEN)
