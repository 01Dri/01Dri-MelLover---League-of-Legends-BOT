import asyncio
from queue import PriorityQueue

from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.FileManager import FileManager
from logger.LoggerConfig import LoggerConfig
from constants.DownloadStates import DownloadStates


def parse_url_youtube(url):
    if not url.startswith("https://www.youtube.com/"):
        raise UrlInvalidFormatYoutubeException("The url must be from YouTube")
    return True


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
        self.current_music_file = None
        self.logger = LoggerConfig()
        parse_url_youtube(self.url)
        self.status_download = DownloadStates.NO_STATUS
        self.file_manager = FileManager(self.path)

    async def add_music_queue_to_download(self):
        if is_playlist_link(self.url):
            self.get_all_urls_playlist_and_add_queue()
        else:
            self.get_url_track_solo_and_add_queue()
        return self

    async def download_musics_on_queue(self):
        while self.get_quantity_musics_on_queue() > 0:
            self.url = self.queue.get()
            await self.download_music(self.url)
            self.logger.get_logger_info_level().info(f'QUANTITY FILES DOWNLOADED: {self.count_download_music + 1} ')
        # self.reset_count()

    def get_url_track_solo_and_add_queue(self):
        try:
            self.track_pytube = YouTube(self.url)
            self.queue.put(self.url)
            return self.track_pytube
        except RegexMatchError:
            raise UrlInvalidFormatYoutubeException("Invalid format url youtube")

    def get_all_urls_playlist_and_add_queue(self):
        self.track_pytube = Playlist(self.url)
        for url in self.track_pytube.video_urls:
            self.queue.put(url)
        return self.track_pytube.video_urls

    async def download_music(self, url):
        self.current_music_file = YouTube(url)
        audio_stream = self.get_only_audio_stream_by_url()
        self.logger.get_logger_info_level().info(f"DOWNLOADING MUSIC: {self.current_music_file.title}")
        filename = self.current_music_file.title + ".mp4"
        if await self.file_manager.verify_if_file_exist(filename):
            self.status_download = DownloadStates.SKIPPED
            self.reset_counting_downloaded_files()
            return
        self.status_download = DownloadStates.IN_PROGRESS
        try:
            await self.download_file(audio_stream, self.path)
            self.status_download = DownloadStates.FINISH
            self.logger.get_logger_info_level().info(
                f'DOWNLOAD COMPLETE: {self.current_music_file.title}, SIZE: {audio_stream.filesize_mb} MB, STATUS '
                f'DOWNLOAD STATUS: {self.get_status_download()}')
            self.count_download_music += 1

            return self
        except Exception as e:
            self.status_download = DownloadStates.ERROR
            self.logger.get_logger_info_error().error(
                f'DOWNLOAD ERROR: {self.current_music_file.title}, EXCEPTION: {str(e)}, STATUS '
                f'DOWNLOAD STATUS: {self.get_status_download()}')

    async def download_file(self, audio_stream, path):
        try:
            await asyncio.to_thread(audio_stream.download(path))  # run asynchronous downloading file
        except Exception as e:
            self.logger.get_logger_info_error().error(str(e))

    def get_quantity_musics_on_queue(self):
        return int(self.queue.qsize())

    def get_only_audio_stream_by_url(self):
        audio_stream_pytube = self.current_music_file.streams.filter(
            only_audio=True).first()
        return audio_stream_pytube

    def reset_counting_downloaded_files(self):
        self.count_download_music = 0

    def get_status_download(self):
        return self.status_download.get_status_name()

    def get_quantity_musics_on_queue(self):
        return int(self.queue.qsize())

    def get_quantity_files_downloaded(self):
        return self.count_download_music
