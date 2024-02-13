from services.league_of_legends_account.LeagueServicesDB import LeagueDB
from services.league_of_legends_account.LolServices import LolServices


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client

    async def handler_commands(self, ctx):
        if ctx.author == self.client.user:
            return
        content_message = ctx.content.lower()
        if content_message.startswith("!accountlol-"):
            lol_services = LolServices(ctx, content_message)
            lol_instance = await lol_services.fetch_account_info()
            if "save" in content_message:
                service_repository_account = LeagueDB()
                service_repository_account.save_account(ctx.author, lol_instance)
                await lol_services.account_lol(ctx)
                return
            await lol_services.account_lol(ctx)
            return

        if content_message == "!accountlol":
            service_repository_account = LeagueDB()
            account_instance = service_repository_account.get_account(ctx.author)
            lol_services = LolServices(ctx, None)
            lol_services.entity_account = account_instance
            await lol_services.account_lol(ctx)



