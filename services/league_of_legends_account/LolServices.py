import os
from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.RiotInvalidNickName import RiotInvalidNickName
from exceptions.league_of_legends_exceptions.RiotResponseError import RiotResponseError
from factory.LolFactory.FactoryAccountLol import FactoryLolAccount
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot
from logger.LoggerConfig import LoggerConfig
from view.view_league_of_legends.ViewEmbedLol import get_embed_account_lol, get_embed_error_get_account_lol, \
    get_embed_account_lol_without_solo_duo_info
from dotenv import load_dotenv


class LolServices:

    def __init__(self, ctx, nick, queue_type):
        self.entity_account = None
        self.lol_api_services = None
        self.nick = nick
        self.logger = LoggerConfig()
        self.queue = queue_type
        load_dotenv()
        self.TOKEN_RIOT = os.getenv("TOKEN_RIOT")

    async def account_lol(self, ctx):
        try:
            await self.fetch_account_info()
            await self.send_view_account_info(ctx, self.entity_account)
        except RiotResponseError:
            await self.handle_riot_response_error(ctx, f"Account with the nick:{self.nick} not found!!!")
        except RiotInvalidNickName:
            await self.handle_riot_response_error(ctx, f"Please report the tag line '#' to view your account")

    async def send_view_account_info(self, ctx, entity_account: AccountLoL):
        if entity_account.tier == "UNRANKED":
            await get_embed_account_lol_without_solo_duo_info(ctx, entity_account, self.queue)
            self.logger.get_logger_info_level().info(f"LEAGUE OF LEGENDS ACCOUNT OF: {self.nick} DISPLAYED")
            return
        await get_embed_account_lol(ctx, entity_account, self.queue)
        self.logger.get_logger_info_level().info(f"LEAGUE OF LEGENDS ACCOUNT OF: {self.nick} DISPLAYED")

    async def fetch_account_info(self):
        self.lol_api_services = ApiRiot(self.nick, self.TOKEN_RIOT, self.queue)
        account_info = self.lol_api_services.get_all_info_account_league()
        self.entity_account = FactoryLolAccount(account_info).get_account_lol_instance()

    async def handle_riot_response_error(self, ctx, message):
        await get_embed_error_get_account_lol(ctx, message)
