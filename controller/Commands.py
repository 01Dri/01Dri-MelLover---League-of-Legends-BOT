import re
from exceptions.OptionCommandLeagueInvalid import OptionCommandLeagueInvalid
from services.league_of_legends_account.LeagueServicesDB import LeagueServicesDB
from services.league_of_legends_account.LolServices import LolServices
from services.league_of_legends_account.gpt.LeagueAccountGPT import LeagueAccountGPT
from view.view_league_of_legends.ViewEmbedLol import get_embed_error, get_embed_tips_gpt


class BotCommands:

    def __init__(self, client) -> None:
        self.client = client
        self.options_account_lol = ["save", "delete"]
        self.options_account_lol_db_options = ["tips"]
        self.message = None
        self.option = None
        self.ctx = None

    async def handler_commands(self, ctx):
        self.ctx = ctx
        if ctx.author == self.client.user:
            return
        self.message = ctx.content.lower()
        if self.message.startswith("!accountlol-"):
            await self.fetch_option_league_command()
            lol_services = LolServices(self.ctx, self.message)
            if self.option == "save":
                await self.command_lol_with_save_option()
            if self.option == "delete":
                return
            await lol_services.get_league_account()

        if self.message == "!accountlol":
            service_repository_account = LeagueServicesDB(ctx)
            account_instance = await service_repository_account.get_account(ctx.author)
            lol_services = LolServices(self.ctx, None)
            await lol_services.send_embeds_discord_message(ctx, account_instance)

        if self.message == "!accountlol -tips":
            gpt = LeagueAccountGPT()
            service_repository_account = LeagueServicesDB(ctx)
            account_instance = await service_repository_account.get_account(ctx.author)
            await get_embed_tips_gpt(ctx, account_instance, gpt.get_tips(account_instance))

    async def command_lol_with_save_option(self):
        lol_services = LolServices(self.ctx, self.message)
        lol_instance = await lol_services.get_league_account()
        service_repository_account = LeagueServicesDB(self.ctx)
        await service_repository_account.save_account(self.ctx.author, lol_instance)
        return

    async def fetch_option_league_command(self):
        pattern = r'#\w+\s*-(\w+)'
        matches = re.findall(pattern, self.message)
        if matches:
            self.option = matches[0]
            if self.option not in self.options_account_lol:
                await get_embed_error(self.ctx, "Option invalid", f"The option: {self.option} is invalid!!!")
                raise OptionCommandLeagueInvalid("Invalid option")
