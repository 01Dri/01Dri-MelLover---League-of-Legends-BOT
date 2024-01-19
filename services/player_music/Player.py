import asyncio
import time

import discord
from pytube import YouTube

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
        self.factory = None
        self.current_status_player = PlayerMusicStatus.SILENCE
        self.logger = LoggerConfig()

    async def connect_bot(self):
        self.voice_channel = self.ctx.author.voice.channel
        try:
            self.voice_client = await self.voice_channel.connect()
            return self
        except Exception as e:
            pass

    async def play(self):
        self.factory = FactoryDownloader(self.path, self.url_music)
        while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
            await asyncio.sleep(1)
        queue = await self.get_queue_by_downloader()
        while int(queue.qsize()) >= 1:
            current_url = queue.get()
            downloader = self.get_downloader()
            file_music = await downloader.download_music(current_url)
            url_info = downloader.get_info_track_by_url(current_url)
            self.voice_client.play(discord.FFmpegPCMAudio(file_music))
            self.current_status_player = PlayerMusicStatus.PLAYING
            self.logger.get_logger_info_level().info(
                f'PLAYER PLAYING NOW: {url_info.title} LENGTH TRACK: {url_info.length}, AUTHOR: {url_info.author}')
            while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
                await asyncio.sleep(1)
            self.set_status_player(PlayerMusicStatus.SILENCE)
            self.logger.get_logger_info_level().info(f'PLAYER FINISH SONG, CURRENT STATUS: {self.get_status_player()}')
            pass

    def pause(self):
        self.current_status_player = PlayerMusicStatus.PAUSE
        self.voice_client.pause()

    async def get_queue_by_downloader(self):
        downloader = self.factory.get_downloader()
        await downloader.add_music_queue_to_download()
        queue = downloader.get_queue()
        return queue

    def get_downloader(self):
        return self.factory.get_downloader()

    ##       self.voice_client.play(discord.FFmpegPCMAudio(os.path.join(self.path, music_file)))
    ##     self.current_status_player = PlayerMusicStatus.PLAYING
    ##    while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
    ##      await asyncio.sleep(1)
    ##     self.voice_client.stop()

    def get_status_player(self):
        return self.current_status_player.get_status_name()

    def set_status_player(self, status):
        self.current_status_player = status

    def get_info_track_by_url(self, url):
        pytube_track = YouTube(url)
        return pytube_track

    def set_url(self, url):
        self.url_music = url
