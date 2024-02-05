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
        if content_message.startswith("!accountlol"):
            queue = await extract_queue(ctx, content_message)
            nick = await extract_nick(ctx, queue)
            lol_services = LolServices(ctx, nick, queue)
            i = 0
            while (i < 40):
                await lol_services.account_lol(ctx)
                i += 1


async def extract_nick(ctx, queue):
    parts = ctx.content.split()
    if len(parts) > 1:
        nickname = urllib.parse.quote(" ".join(parts[1:]))
        return nickname
    await get_embed_error_get_account_lol(ctx, "Nick doesn't can be none")
    raise Exception("Nick doesn't can be none")


async def extract_queue(ctx, command):
    if "-" in command:
        if "-solo" in command:
            return "RANKED_SOLO_5x5"
        elif "-flex" in command:
            return "RANKED_FLEX_SR"
    await get_embed_error_get_account_lol(ctx, "Queue doesn't can be none")
    raise Exception("Queue doesn't can be none")
