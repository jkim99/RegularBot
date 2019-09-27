"""
regular.py
it's anything bot
"""

from datetime import datetime
from reddit import REDDIT
# from spotify import SPOTIFY
from creds import BOT_TOKEN
import discord


PREFIX = '.'


class MyClient(discord.Client):
    visited_posts = []

    async def on_ready(self):
        self.reddit = REDDIT()
        print('Logged in as' + self.user.name)
        print('User ID: ' + self.user.id)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # this line right here gets the time
        t = datetime.today().strftime('[%Y-%m-%d-%H:%M]')

        # this adds the message to the log
        log = open('log.txt', 'a')
        log.write('{}{} {}\n'.format(t, message.content, str(message.author)))
        log.close()

        # Ping --> Pong
        if message.content.startswith(PREFIX + 'ping'):
            await message.channel.send('pong!')

        # Closes bot
        elif message.content.startswith(PREFIX + 'stop'):
            await message.channel.send('Stopping...')
            await self.logout()

        # Takes suggestions and writes it to a file
        elif message.content.startswith(PREFIX + 'suggestion'):
            file = open('suggestions.txt', 'a')
            content = message.content.replace(PREFIX + 'suggestion', '')
            file.write('\n{}{} [{}]'.format(t, content, str(message.author)))
            file.close()
            await message.channel.send('Thank you for the suggestion')

        # Gets meme from the reddit module
        elif message.content.startswith(PREFIX + 'meme'):
            await message.channel.send(self.reddit.meme(message))

        # Plays music
        elif message.content.startswith(PREFIX + 'play'):
            channel = self.get_channel('General')
            await discord.VoiceChannel.connect(channel)


def main():
    client = MyClient()
    client.run(BOT_TOKEN)


if __name__ == '__main__':
    main()
