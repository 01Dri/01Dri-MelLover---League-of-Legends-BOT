import asyncio
import time

from services.league_of_legends_account.LolServices import LolServices
from services.player_music.Player import Player
from services.player_music.YoutubeDownloader import YoutubeDownloader
from constants.DownloadStates import DownloadStates
from constants.Contants import DEFAULT_PATH_FOLDER_DOWNLOAD

class BotCommands:

    def __init__(self, client) -> None:
        self.client = client
        self.guid_musics = {}  # This is for each user to have their own instance of PlayerMusic by
        self.player = Player(DEFAULT_PATH_FOLDER_DOWNLOAD, None, None, None)

    async def handler_commands(self, ctx):
        if ctx.author == self.client.user:
            return
        content_message = ctx.content.lower()
        if content_message.startswith("!contalol"):
            lol_services = LolServices(ctx)
            inicio = time.time()
            await lol_services.get_account_lol_info(ctx)
            fim = time.time()
            tempo_execucao = fim - inicio
            print(f"A função levou {tempo_execucao} segundos para executar.")

        if content_message.startswith("!m"):
            youtube_downloader = YoutubeDownloader(
                f"C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\{ctx.guild.id}",
                None)
            player = Player(
                f"C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\{ctx.guild.id}", ctx,
                None, None)

            if "play" in content_message:
                message_music = ctx.content.split()
                url_music = message_music[1]
                youtube_downloader.url = url_music
                if "youtube" in url_music:
                    youtube_downloader = YoutubeDownloader(f"C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\{ctx.guild.id}", url_music)
                    await youtube_downloader.add_music_queue_to_download()
                    queue = youtube_downloader.get_queue()
                    player = Player(
                          f"C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\{ctx.guild.id}", ctx, queue, url_music)
                    await player.connect_bot()
                    await player.play()

              ##  await youtube_download.add_music_queue_to_download()

                # Run download and play tasks concurrently
               ## download_task = asyncio.create_task(youtube_download.download_musics_on_queue())
               ## await asyncio.gather(download_task, self.play_music(ctx))

  ##  async def play_music(self, ctx):
    ##    player = Player(
      ##      f"C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\{ctx.guild.id}",
         ##   ctx)
     ##   await player.connect_bot()
      ##  await player.play()
