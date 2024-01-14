import os

import discord


class Player:

    def __init__(self, path, ctx):
        self.path = path
        self.ctx = ctx
        self.voice_channel = None
        self.voice_client = None

    async def connect_bot(self):
        self.voice_channel = self.ctx.author.voice.channel
        self.voice_client = await self.voice_channel.connect()
        return self

    def play(self):
        files = os.listdir(self.path)
        for music_file in files:
            self.voice_client.play(discord.FFmpegPCMAudio(os.path.join(self.path, music_file)))
