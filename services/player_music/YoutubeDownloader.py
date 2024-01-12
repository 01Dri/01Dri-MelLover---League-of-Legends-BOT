from queue import PriorityQueue

from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.FileManager import FileManager
from logger.LoggerConfig import LoggerConfig


def parse_url_youtube(url):
    url_splited = url.split()
    if len(url_splited) > 1:
        new_url = url_splited[1]
        if not new_url.startswith("https://www.youtube.com/"):
            raise UrlInvalidFormatYoutubeException("The url must be from YouTube")
        return True
    raise UrlInvalidFormatYoutubeException("The url must be from YouTube")


def is_playlist_link(url):
    if "https://www.youtube.com/playlist" in url:
        return True


class YoutubeDownloader:

    def __init__(self, path, url):
        self.path = path  # Folder to save downloaded musics
        self.track_pytube = None
        self.queue = PriorityQueue()
        self.url = url
        self.count_download_music = 0
        self.file_manager = FileManager(self.path)
        self.current_music_file = None
        self.logger = LoggerConfig()

    def add_music_queue_download(self):
        parse_url_youtube(self.url)
        if is_playlist_link(self.url):
            self.get_all_urls_playlist()
        else:
            self.get_url_track_solo()
        self.download_musics_on_queue()
        return self

    def get_url_track_solo(self):
        try:
            self.track_pytube = YouTube(self.url)
            self.queue.put(self.url)
            return self.track_pytube
        except RegexMatchError:
            raise UrlInvalidFormatYoutubeException("Invalid format url youtube")

    def get_all_urls_playlist(self):
        self.track_pytube = Playlist(self.url)
        for url in self.track_pytube.video_urls:
            self.queue.put(url)
        return self.track_pytube

    def download_musics_on_queue(self):
        while self.get_quantity_musics_on_queue() > 0:
            self.current_music_file = YouTube(self.queue.get())
            audio_stream = self.get_only_audio_stream_by_url()
            self.logger.get_logger_info_level().info(f"DOWNLOADING MUSIC: {self.current_music_file.title}")
            audio_stream.download(self.path)
            self.logger.get_logger_info_level().info(
                f'DOWNLOADING COMPLETE: {self.current_music_file.title}, SIZE: {audio_stream.filesize_mb} MB')
            self.count_download_music += 1
        self.reset_count()

    def get_quantity_musics_on_queue(self):
        return int(self.queue.qsize())

    def get_only_audio_stream_by_url(self):
        audio_stream_pytube = self.current_music_file.streams.filter(
            only_audio=True).first()
        return audio_stream_pytube

    def reset_count(self):
        self.count_download_music = 0

    # def create_entity_track(self):
    #     track_entity = YoutubeTrack(
    #         self.track_pytube.title,
    #         None,
    #         self.track_pytube.length,
    #         self.track_pytube.author
    #     )
    #     return track_entity
    #
    # def verify_downloaded_music_file_exist(self, track_entity):
    #     print(track_entity)
    #     if track_entity is None:
    #         track_entity = self.create_entity_track()
    #     path_music_name = f'{track_entity.title}.mp4'
    #     full_path_final = os.path.join(self.path, path_music_name)
    #     if os.path.exists(full_path_final):
    #         return True
    #     raise NotFoundMusicFile("")
