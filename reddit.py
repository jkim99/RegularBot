"""
reddit.py
the reddit module
"""
import praw
import urllib.request
import creds as r


class REDDIT():
    """docstring for REDDIT"""
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=r.client_id,
            client_secret=r.client_secret,
            username=r.username,
            password=r.password,
            user_agent=r.user_agent
        )
        self.__load_visited__()

    def __load_visited__(self):
        v = []
        with open('visited.txt') as f:
            v = f.readlines()
        self.visited_posts = [x.strip for x in v]

    def meme(self, message):
        dankmemes = self.reddit.subreddit('dankmemes').hot()
        for post in dankmemes:
            if post.url not in self.visited_posts:
                self.__add_visited__(post.url)
                # page = urllib.request.urlopen(post.url)
                # html = page.read().decode("utf8")
                # image = self.__image_scrape__(html)
                return post.url

    def __image_scrape__(self, html):
        html = html[html.index('i.redd.it'), len(html) - 1]
        print(html)

    def __add_visited__(self, post_url):
        print("adding visited " + post_url)
        self.visited_posts.append(post_url)
        v = open('memes/visited.txt', 'a')
        v.write(post_url + '\n')
        v.close()
