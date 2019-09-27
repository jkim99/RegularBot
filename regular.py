"""
regular.py
it's anything bot
"""

import discord
# import praw
# import random

BOT_TOKEN = 'NjI2OTM2ODY4MzM1Nzc5ODY1.XY1XKQ.jOauRwP_eE7njBuLwnGKvbc51h4'
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
        if message.content == '_ping':
            await message.channel.send('pong')

        # this takes suggestions and writes it to a file
        if message.content.contains(PREFIX + "suggestions"):
            file = open("suggestions.txt", "w")
            content = message.content
            file.append(content.replace(PREFIX + "suggestions", ""))
            file.close()

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
