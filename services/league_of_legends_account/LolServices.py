import urllib.parse
from constants.Contants import TOKEN_RIOT
from entities.entities_discord_account.DiscordAccount import DiscordAccount
from exceptions.league_of_legends_exceptions.RiotInvalidNickName import RiotInvalidNickName
from exceptions.league_of_legends_exceptions.RiotResponseError import RiotResponseError
from factory.LolFactory.FactoryAccountLol import FactoryLolAccount
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot
from view.view_league_of_legends.ViewEmbedLol import ViewEmbedLol
from logger.LoggerConfig import LoggerConfig


class LolServices:

    def __init__(self, ctx):
        self.account_discord = DiscordAccount(ctx.author)
        self.lol_api_services = None
        self.view_embeds = ViewEmbedLol()
        self.nick = None
        self.logger = LoggerConfig()

    async def get_account_lol_info(self, ctx):
        try:
            self.nick = self.parser_nick_command(ctx)
            self.lol_api_services = ApiRiot(self.nick, TOKEN_RIOT)
            entity_account = FactoryLolAccount(self.lol_api_services.get_all_info_account_league()).get_account_lol_instance()
            await self.send_view_account_info(ctx, entity_account)
        except RiotResponseError:
            await self.view_embeds.get_embed_error_get_account_lol(ctx, f"Conta com o nick:{self.nick} não foi encontrada")
        except RiotInvalidNickName:
            await self.view_embeds.get_embed_error_get_account_lol(ctx, f"Por favor informe a tag line '#' para "
                                                                        f"visualizar sua conta")

    def parser_nick_command(self, ctx):
        parts = ctx.content.split()
        if len(parts) > 1 and parts[0] == "!contalol":
            self.nick = urllib.parse.quote(" ".join(parts[1:]))
            return self.nick
        raise Exception("Nick doesn't can be none")

    async def send_view_account_info(self, ctx, entity_account):
        if entity_account.tier == "UNRANKED":
            await self.view_embeds.get_embed_account_lol_without_solo_duo_info(ctx, entity_account.nick,
                                                                               entity_account.level,
                                                                               entity_account.op_gg,
                                                                               entity_account.best_champ)
            self.logger.get_logger_info_level().info(f"LEAGUE OF LEGENDS ACCOUNT OF: {self.nick} DISPLAYED")
            return

        await self.view_embeds.get_embed_account_lol(ctx, entity_account.nick, entity_account.league,
                                                     entity_account.tier, entity_account.level,
                                                     entity_account.winrate, entity_account.pdl,
                                                     entity_account.op_gg, entity_account.best_champ)
        self.logger.get_logger_info_level().info(f"LEAGUE OF LEGENDS ACCOUNT OF: {self.nick} DISPLAYED")
