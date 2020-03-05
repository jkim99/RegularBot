import youtube_dl
import os


class YOUTUBE:
    def __init__(self):
        self.queue = []

    def queue_song(self, url):
        self.queue.append(url)

    def download(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.queue.pop()])
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                return str(file)

    def clear_mp3(self):
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                os.remove(file)


if __name__ == '__main__':
    y = YOUTUBE()
    y.queue_song('https://www.youtube.com/watch?v=iW06RYlooGc')
    y.download()
    y.clear_mp3()
