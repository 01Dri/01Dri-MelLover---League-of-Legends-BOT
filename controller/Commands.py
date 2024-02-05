import time
import urllib.parse

from services.league_of_legends_account.LolServices import LolServices
from view.view_league_of_legends.ViewEmbedLol import get_embed_error_get_account_lol


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client

    async def handler_commands(self, ctx):
        if ctx.author == self.client.user:
            return

        content_message = ctx.content.lower()
        if content_message.startswith("!accountlol-solo"):
            lol_services = LolServices(ctx, await parser_nick_command_lol(ctx))
            inicio = time.time()
            await lol_services.account_lol(ctx)
            fim = time.time()
            tempo_execucao = fim - inicio
            print(f"A função levou {tempo_execucao} segundos para executar.")


async def parser_nick_command_lol(ctx):
    parts = ctx.content.split()
    if len(parts) > 1 and parts[0] == "!accountlol-solo":
        nick = urllib.parse.quote(" ".join(parts[1:]))
        return nick
    await get_embed_error_get_account_lol(ctx, "Nick doesn't can be none")
