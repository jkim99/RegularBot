#!/usr/bin/python3

"""
reddit.py
the reddit module
"""
import praw
import urllib.request
import creds as r
import requests


class REDDIT:
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
        with open('memes/visited.txt') as f:
            v = f.readlines()
        self.visited_posts = [x.strip for x in v]

    # Returns a meme as .png or .jpeg
    def get_meme(self):
        # Get posts and find one unread
        dankmemes = self.reddit.subreddit('dankmemes').hot(limit=100)
        for post in dankmemes:
            if post.url not in self.visited_posts:
                self.__add_visited__(post.url)
                image_url = post.url
                break

        # Filter image file types
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += 'jpeg'
            extension = '.jpeg'
        else:
            return -1

        # Get & return image. allow_redirects=False stops removed post images
        image = requests.get(image_url, allow_redirects=False)
        if image.status_code == 200:
            with open('meme' + extension, mode='wb') as meme_file:
                meme_file.write(image.content)
            return 'meme' + extension
        else:
            return -2

    def __image_scrape__(self, html):
        html = html[html.index('i.redd.it'), len(html) - 1]
        print(html)

    def __add_visited__(self, post_url):
        print("adding visited " + post_url)
        self.visited_posts.append(post_url)
        v = open('memes/visited.txt', 'a')
        v.write(post_url + '\n')
        v.close()
