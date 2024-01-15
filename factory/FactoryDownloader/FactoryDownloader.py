from services.player_music.YoutubeDownloader import YoutubeDownloader


class FactoryDownloader:

    def __init__(self, path, url):
        self.url = url
        self.path = path

    def get_downloader(self):
        if self.url.startswith("https://www.youtube.com"):
            youtube_downloader = YoutubeDownloader(self.path, self.url)
            return youtube_downloader
        ## --- OTHERS FACTORYS HERE
