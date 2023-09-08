import asyncio
import os
import shutil
import discord

from pytube import Playlist
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

from constants.Contants import DEFAULT_PATH
from constants.Contants import LINK_FOR_YOUTUBE
from constants.Contants import PLAYLIST_LINK
from constants.Contants import LINK_MUSIC_UNIT_FOR_YOUTUBE

from entities.Track import Track
from entities.PlaylistEntity import PlaylistEntity

from embeds.Embeds import create_embed_for_error_link_music
from embeds.Embeds import create_embed_for_error_voice_connect
from embeds.Embeds import create_embed_for_skip
from embeds.Embeds import create_embed_for_pause
from embeds.Embeds import create_embed_for_resume
from embeds.Embeds import create_embed_for_stop

class PlayerMusic:
    def __init__(self, ctx):

        self.track_entity = None
        self.track_by_pytube = None
        self.playlist_entity = None
        self.ctx = ctx
        self.playlist_queue_pytube = None
        self.playlist_songs = []
        self.pause_status = False
        self.already_playing = False
        self.skip_status = False
        self.voice_channel = None
        self.voice_client = None
        self.PATH = DEFAULT_PATH
        self.i = 0
        self.embed_playlist = None
        self.playlist_status = False
        self.music_unit_status = False
        self.download_fail = True

    async def load_songs(self, ctx):
        global playlist_desc
        parts_message = ctx.content.split()
        url = parts_message[1]
        print(url)
        if LINK_FOR_YOUTUBE in url:
            if PLAYLIST_LINK in url:
                print("passou aq")
                try:
                    self.playlist_queue_pytube = Playlist(url)
                    self.music_unit_status = False
                    self.playlist_status = True
                    try:
                        playlist_desc = self.playlist_queue_pytube.description
                    except:
                        playlist_desc = "Sem descrição"
                    self.playlist_entity = PlaylistEntity(self.playlist_queue_pytube.title,
                                                  self.playlist_queue_pytube.length,
                                                  "teste", "teste", playlist_desc)
                            
                    for track in self.playlist_queue_pytube:
                        self.playlist_songs.append(track)
                        self.download_fail = False
                except KeyError:
                    print("Link inválido")
                    self.download_fail = True
                    await ctx.reply(embed=create_embed_for_error_link_music())
                    
          
            if LINK_MUSIC_UNIT_FOR_YOUTUBE in url:
                print("passou aq")
                self.playlist_status = False
                self.music_unit_status = True
                try:
                    self.track_by_pytube = YouTube(url)
                    self.track_entity = Track(self.track_by_pytube.title, self.track_by_pytube.length,
                                            1, ctx.author, ctx.author.display_avatar)
                    self.playlist_songs.append(url)
                    self.download_fail = False

                except VideoUnavailable:
                    print("Link inválido")
                    self.download_fail = True
                    await ctx.reply(embed=create_embed_for_error_link_music())
        else:
            await ctx.reply(embed=create_embed_for_error_link_music())
                    
        
        
    async def download_music(self, ctx, url):
            track_api_pytube = YouTube(url)
            self.track_entity = Track(track_api_pytube.title, track_api_pytube.length, url, ctx.author,
                                    ctx.author.display_avatar)
            audio_stream = YouTube(self.track_entity.url).streams.filter(only_audio=True).first()
            audio_stream.download(await self.get_folder_musics(ctx))
            print(audio_stream.default_filename)
            audio_source = discord.FFmpegPCMAudio(os.path.join(await self.get_folder_musics(ctx), audio_stream.default_filename))
            return audio_source
    
    async def connect_bot_and_load_songs(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.reply(embed=create_embed_for_error_voice_connect())
        else:
            self.voice_channel = ctx.author.voice.channel
            try:
                self.voice_client = await self.voice_channel.connect()
                await self.load_songs(ctx)
            except discord.DiscordException:
                await self.load_songs(ctx)
        return

    async def verify_status(self):
        while self.pause_status or self.voice_client.is_playing():
            await asyncio.sleep(1)

        self.pause_status = False
        self.already_playing = False
        return False


    async def play_music(self, ctx):
        await self.connect_bot_and_load_songs(ctx)
        await self.verify_how_to_use_embed(ctx)
        while self.playlist_songs:
            try:
                file = await self.download_music(ctx, self.playlist_songs[self.i])
            except:
                return
            try:
                if not self.skip_status:
                    await asyncio.sleep(2)
                    self.voice_client.play(file)
                    self.i += 1  
                    if self.track_entity is None:
                        return
                    else:
                        await ctx.channel.send(embed=self.track_entity.get_embed_for_track_current())
                        await self.verify_status()
                else:
                    self.skip_status = False

            except discord.DiscordException as e:
                print(e)
                await asyncio.sleep(180)
                break
    async def pause(self, ctx):

        self.voice_client.pause()
        self.pause_status = True
        await ctx.reply(embed=create_embed_for_pause())

    async def resume(self, ctx):
        self.voice_client.resume()
        self.pause_status = False
        await ctx.reply(embed=create_embed_for_resume())

    async def skip(self, ctx):
        self.voice_client.stop()
        self.skip_status = True
        await ctx.reply(embed=create_embed_for_skip(self.track_entity.name))
        

    async def stop(self, ctx):
        await self.disconnect(ctx)
        self.pause_status = False
        self.already_playing = False
        await ctx.reply(embed=create_embed_for_stop())


    async def disconnect_for_away(self, ctx):
        if self.voice_client == None:
            return
        if not self.voice_client.is_playing():
            await asyncio.sleep(180)
            await self.disconnect(ctx)

        self.pause_status = False
        self.already_playing = False
        return False

    async def disconnect(self, ctx):
        await self.voice_client.disconnect()
        self.playlist_songs.clear()
        self.i = 0
        self.pause_status = False
        await asyncio.sleep(2)
        await self.remove_mp4_files(ctx)

    async def remove_mp4_files(self, ctx):
        shutil.rmtree(await self.get_folder_musics(ctx))


    async def get_folder_musics(self, ctx):
        folder_for_musics = f"{ctx.guild.id}"
        folder_for_musics_path = os.path.join(self.PATH, folder_for_musics)

        return folder_for_musics_path

    async def verify_how_to_use_embed(self, ctx):
        if self.download_fail:
            return
         
        if self.playlist_status:
            await ctx.channel.send(embed=self.playlist_entity.get_embed_response())
        elif self.music_unit_status:
            if self.track_entity is None:
                return
            else:
                await ctx.channel.send(embed=self.track_entity.get_embed_for_track())

