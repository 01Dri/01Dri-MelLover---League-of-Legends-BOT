import time

from constants.Contants import DEFAULT_PATH_FOLDER_DOWNLOAD
from constants.PlayerStatus import PlayerMusicStatus
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
        if content_message.startswith("!contalol"):
            await self.handler_lol_services(ctx)
        if content_message.startswith("!m"):
            author_id = ctx.author.id
            if author_id in self.guid_musics:
                self.player = self.guid_musics[ctx.author.id]
            else:
                self.player = Player("/home/dridev/Downloads", ctx, None)
                await self.player.connect_bot()
                self.guid_musics[author_id] = self.player
            await self.handler_player_music(ctx, content_message)

    async def handler_lol_services(self, ctx):
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
            await self.guid_musics[ctx.author.id].add_queue(url_music)
            print(self.guid_musics[ctx.author.id].get_status_player())
            if self.guid_musics[ctx.author.id].get_status_player() == PlayerMusicStatus.PLAYING.get_status_name():
                self.guid_musics[ctx.author.id].add_queue(url_music)
            else:
                await self.guid_musics[ctx.author.id].play()

        if content_message.startswith("!mpause"):
            print("PAUSADO!")
            self.guid_musics[ctx.author.id].pause()
