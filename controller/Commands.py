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
            await self.handler_lol_srvices(ctx)
        if content_message.startswith("!m"):
            await self.handler_player_music(ctx, content_message)

    async def handler_lol_srvices(self, ctx):
        lol_services = LolServices(ctx)
        inicio = time.time()
        await lol_services.get_account_lol_info(ctx)
        fim = time.time()
        tempo_execucao = fim - inicio
        print(f"A função levou {tempo_execucao} segundos para executar.")

    async def handler_player_music(self, ctx, content_message):
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
