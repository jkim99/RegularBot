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
    user_agent='Regular Bot Mk01'
)
PREFIX = '!'


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

        if message.content.startswith(PREFIX + 'meme'):
            dankmemes = reddit.subreddit('dankmemes').hot()
            for post in dankmemes:
                if post.id not in self.visited_posts:
                    await message.channel.send(post.url)
                    self.visited_posts.append(post.id)
                    break


client = MyClient()
client.run(BOT_TOKEN)
