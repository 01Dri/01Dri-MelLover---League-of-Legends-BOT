import time

from services.league_of_legends_account.LolServices import LolServices
from services.player_music.YoutubeDownloader import YoutubeDownloader


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client
        self.guid_musics = {}  # This is for each user to have their own instance of PlayerMusic by

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

        if content_message.startswith("!mplay"):
            youtube_download = YoutubeDownloader(
                "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics\\", ctx.content)
            youtube_download.add_music_queue_download()
