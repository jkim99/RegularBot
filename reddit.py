"""
reddit.py
the reddit module
"""
import praw
import urllib.request


class REDDIT():
    """docstring for REDDIT"""
    def __init__(self, arg):
        self.reddit = praw.Reddit(
            client_id='YBh9gOGQzW8GuQ',
            client_secret='hVqgmeKxTqV7pzSgWuIUSlGjDZQ',
            username='TheRegularBot',
            password='@pple314',
            user_agent='Regular Bot Mk01'
        )
        self.visited_posts = []

    def meme(self, message):
        dankmemes = self.reddit.subreddit('dankmemes').hot()
        for post in dankmemes:
            if post.id not in self.visited_posts:
                page = urllib.request.urlopen(post.url)
                html = page.read().decode("utf8")
                print(html)
                # await message.channel.send(post.url)
                # self.visited_posts.append(post.id)
                # break
