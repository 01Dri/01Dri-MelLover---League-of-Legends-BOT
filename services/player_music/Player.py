import asyncio

import discord

from constants.PlayerStatus import PlayerMusicStatus
from factory.FactoryDownloader.FactoryDownloader import FactoryDownloader


class Player:

    def __init__(self, path, ctx, queue, url_music):
        self.path = path
        self.ctx = ctx
        self.voice_channel = None
        self.voice_client = None
        self.current_status_player = PlayerMusicStatus.SILENCE
        self.queue = queue
        self.factory = FactoryDownloader(self.path, url_music)

    async def connect_bot(self):
        self.voice_channel = self.ctx.author.voice.channel
        try:
            self.voice_client = await self.voice_channel.connect()
            return self
        except Exception as e:
            pass

    async def play(self):
        downloader = self.factory.get_downloader()
        while int(self.queue.qsize()) >= 1:
            print(downloader)
            file_music = await downloader.download_music(self.queue.get())
            self.voice_client.play(discord.FFmpegPCMAudio(file_music))
            self.current_status_player = PlayerMusicStatus.PLAYING
            while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
                await asyncio.sleep(1)

    async def pause(self):
        self.current_status_player = PlayerMusicStatus.PAUSE
        await self.voice_client.pause()

    ##       self.voice_client.play(discord.FFmpegPCMAudio(os.path.join(self.path, music_file)))
    ##     self.current_status_player = PlayerMusicStatus.PLAYING
    ##    while self.get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
    ##      await asyncio.sleep(1)
    ##     self.voice_client.stop()

    def get_status_player(self):
        return self.current_status_player.get_status_name()
