import asyncio
import discord

from constants.PlayerStatus import PlayerMusicStatus
from factory.FactoryDownloader.FactoryDownloader import FactoryDownloader
from logger.LoggerConfig import LoggerConfig


class Player:

    def __init__(self, path, ctx, url_music):
        self.path = path
        self.ctx = ctx
        self.url_music = url_music
        self.voice_channel = None
        self.voice_client = None
        self.current_status_player = PlayerMusicStatus.SILENCE
        self.factory_downloader = None
        self.downloader = None
        self.queue = None
        self.logger = LoggerConfig()

    async def connect_bot(self):
        self.voice_channel = self.ctx.author.voice.channel
        try:
            self.voice_client = await self.voice_channel.connect()
            return self
        except Exception as e:
            pass

    async def add_queue(self, url):
        self.factory_downloader = FactoryDownloader(self.path, url)
        self.downloader = self.factory_downloader.get_downloader()
        await self.downloader.add_music_queue_to_download()
        self.queue = self.downloader.get_queue()
        return self.downloader.get_info_track_by_url(url)

    async def play(self):
        while int(self.queue.qsize()) >= 1:
            current_url = self.queue.get()
            file_music = await self.downloader.download_music(current_url)
            url_info = self.downloader.get_info_track_by_url(current_url)
            self.voice_client.play(discord.FFmpegPCMAudio(file_music))  # Bot start the audio file on server
            self.logger.get_logger_info_level().info(
                f'PLAYER PLAYING NOW: {url_info.title} LENGTH TRACK: {url_info.length}, AUTHOR: {url_info.author}')
            while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
                self.set_status_player(PlayerMusicStatus.PLAYING)
                await asyncio.sleep(1)
            self.set_status_player(PlayerMusicStatus.SILENCE)  # After audio file arrives at the end, set status silence
            self.logger.get_logger_info_level().info(f'PLAYER FINISH SONG, CURRENT STATUS: {self.get_status_player()}')
            pass

    def pause(self):
        self.set_status_player(PlayerMusicStatus.PAUSE)  # After audio file arrives at the end, set status silence
        self.voice_client.pause()
        self.logger.get_logger_info_level().info(f'PLAYER PAUSED')

    def get_status_player(self):
        return self.current_status_player.get_status_name()

    def set_status_player(self, status):
        self.current_status_player = status

    def set_url(self, url):
        self.url_music = url
