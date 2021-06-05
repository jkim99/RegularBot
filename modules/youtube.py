import youtube_dl
import os


class YOUTUBE:
    def __init__(self):
        self.queue = []

    def enqueue(self, url):
        self.queue.append(self.download(url))

    def pop_queue(self):
        return self.queue.pop()

    def download(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                return str(file)

    def clear_mp3(self):
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                os.remove(file)

    def print_queue(self):
        return str(self.queue)
