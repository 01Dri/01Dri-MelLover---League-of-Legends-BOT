import time

from constants.Contants import DEFAULT_PATH_FOLDER_DOWNLOAD
from services.league_of_legends_account.LolServices import LolServices
from services.player_music.Player import Player


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client
        self.guid_musics = {}  # This is for each user to have their own instance of PlayerMusic by
        self.player = None

    async def handler_commands(self, ctx):
        if ctx.author == self.client.user:
            return
        content_message = ctx.content.lower()
        self.guid_musics[ctx.author.id] = Player(DEFAULT_PATH_FOLDER_DOWNLOAD, ctx, None)
        if content_message.startswith("!contalol"):
            lol_services = LolServices(ctx)
            inicio = time.time()
            await lol_services.get_account_lol_info(ctx)
            fim = time.time()
            tempo_execucao = fim - inicio
            print(f"A função levou {tempo_execucao} segundos para executar.")

        if content_message.startswith("!mplay"):
            message_music = ctx.content.split()
            url_music = message_music[1]
            self.guid_musics[ctx.author.id].set_url(url_music)
            if "youtube" in url_music:
                await self.guid_musics[ctx.author.id].connect_bot()
                await self.guid_musics[ctx.author.id].play()

        if content_message.startswith("!mpause"):
            if ctx.author.id in self.guid_musics:
                self.guid_musics[ctx.author.id].pause()
            else:
                print(self.guid_musics)
                print("nao")
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
