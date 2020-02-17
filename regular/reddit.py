#!/usr/bin/python3

"""
reddit.py
the reddit module
"""
import praw
from regular import creds
import requests
import time


class REDDIT:
    """docstring for REDDIT"""
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=creds.client_id,
            client_secret=creds.client_secret,
            username=creds.username,
            password=creds.password,
            user_agent=creds.user_agent
        )
        self.visited_posts = []
        self.__load_visited__()

    def __load_visited__(self):
        v = []
        with open('visited.txt') as f:
            v = f.readlines()
        for line in v:
            self.visited_posts.append(line.strip())

    # Returns a meme as .png or .jpeg
    def get_meme(self, subreddit='dankmemes'):
        # Get posts and find one unread
        dankmemes = self.reddit.subreddit(subreddit).hot(limit=100)
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
            return ''

        # Get & return image. allow_redirects=False stops removed post images
        image = requests.get(image_url, allow_redirects=False)
        if image.status_code == 200:
            with open('meme' + extension, mode='wb') as meme_file:
                meme_file.write(image.content)
            return 'meme' + extension
        else:
            return ''

    def __add_visited__(self, post_url):
        print("adding visited " + post_url)
        self.visited_posts.append(post_url)
        v = open('visited.txt', 'a')
        v.write(post_url + '\n')
        v.close()

    def meme_stream(self):
        subreddit = self.reddit.subreddit('memes')
        for post in subreddit.stream.submissions():
            image_url = post.url
            # Filter image file types
            if '.png' in image_url:
                extension = '.png'
            elif '.jpg' in image_url or '.jpeg' in image_url:
                extension = '.jpeg'
            elif 'imgur' in image_url:
                image_url += 'jpeg'
                extension = '.jpeg'
            else:
                continue

            image = requests.get(image_url, allow_redirects=False)
            if image.status_code == 200:
                with open('meme' + extension, mode='wb') as meme_file:
                    meme_file.write(image.content)
                yield 'meme' + extension
            time.sleep(1)

