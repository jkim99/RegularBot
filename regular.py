"""
regular.py
it's anything bot
"""

from datetime import datetime
import discord
import praw
# import random

BOT_TOKEN = 'NjI2OTM2ODY4MzM1Nzc5ODY1.XY1xig.klUPz5__kSkqWxHAoFWs_8KnjKo'
reddit = praw.Reddit(
    client_id='YBh9gOGQzW8GuQ',
    client_secret='hVqgmeKxTqV7pzSgWuIUSlGjDZQ',
    username='TheRegularBot',
    password='@pple314',
    user_agent='Regular Bot Mk.01'
)
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

        # gets the time
        time = datetime.today().strftime('[%Y-%m-%d-%H:%M]')

        # adds the message to the log
        log = open('log.txt', 'a')
        log.write('{}{} {}'.format(time, message.content, str(message.author)))
        log.close()

        # Ping --> Pong
        if message.content.startswith(PREFIX + 'ping'):
            await message.channel.send('pong!')

        # Takes suggestions and writes it to a file
        if message.content.startswith(PREFIX + 'suggestions'):
            file = open('suggestions.txt', 'a')
            content = message.content.replace(PREFIX + 'suggestions', '')
            file.write('\n{}{} [{}]'.format(time, content, str(message.author)))
            file.close()
            await message.channel.send('Thanks for the suggestion')

        # Gets a meme from Reddit and sends it in the chat
        if message.content.startswith(PREFIX + 'meme'):
            dankmemes = reddit.subreddit('dankmemes').hot(limit=100)
            visited = False
            for post in dankmemes:  # Can only iterate with for loop
                visited = post.clicked
                post.url
            memeurl = random.choice(lst)
            await message.channel.send(memeurl)


client = MyClient()
client.run(BOT_TOKEN)
