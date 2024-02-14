from exceptions.FailedToSaveAccountInDatabaseException import FailedToSaveAccountInDatabase
from exceptions.NotFoundAccountLolOnDB import NotFoundAccountLolOnDB
from factory.FactoryAccountLol import FactoryLolAccount
from repositories.league_repository.LeagueRepository import LeagueRepository
from view.view_league_of_legends.ViewEmbedLol import get_embed_error


class LeagueServicesDB:

    def __init__(self, ctx):
        self.league_repository = LeagueRepository()
        self.ctx = ctx

    async def save_account(self, nick_discord, account_instance):
        try:
            self.league_repository.save_account(nick_discord, account_instance)
        except FailedToSaveAccountInDatabase as e:
            await get_embed_error_db(self.ctx, "Failed to save account on DB", e)

    async def get_account(self, nick_discord):
        try:
            hash_result = self.league_repository.get_account_by_nick(nick_discord)
            factory_account = FactoryLolAccount(hash_result)
            return factory_account.get_account_lol_instance()
        except NotFoundAccountLolOnDB as e:
            await get_embed_error(self.ctx, "Account not found on DB", e)



