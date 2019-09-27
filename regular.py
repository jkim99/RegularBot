"""
regular.py
it's anything bot
"""

from datetime import datetime
import discord
# import praw
# import random

BOT_TOKEN = 'NjI2OTM2ODY4MzM1Nzc5ODY1.XY1xig.klUPz5__kSkqWxHAoFWs_8KnjKo'
# reddit = praw.Reddit(
#     client_id='',
#     client_secret='',
#     username='',
#     password='',
#     user_agent=''
# )
PREFIX = '!'


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')
        log = open('log.txt', 'a')
        log.write('{} {} {}'.format(t, message.content, str(message.author)))
        log.close()

        # Ping --> Pong
        if message.content.startswith(PREFIX + 'ping'):
            await message.channel.send('pong!')

        # Takes suggestions and writes it to a file
        if message.content.startswith(PREFIX + 'suggestions'):
            file = open('suggestions.txt', 'a')
            content = message.content.replace(PREFIX + 'suggestions', '')
            file.write('\n{} {} [{}]'.format(t, content, str(message.author)))
            file.close()
            await message.channel.send('Thank you for the suggestion')

        # TODO Fix reddit bot
        # if message.content.startswith('_meme'):
        #     dankmemes = reddit.subreddit('dankmemes').hot(limit=100)
        #     lst = []
        #     for post in dankmemes:
        #         lst.append(post.url)
        #     memeurl = random.choice(lst)
        #     await message.channel.send(memeurl)


client = MyClient()
client.run(BOT_TOKEN)
