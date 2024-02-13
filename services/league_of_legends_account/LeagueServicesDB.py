from factory.FactoryAccountLol import FactoryLolAccount
from repositories.league_repository.LeagueRepository import LeagueRepository


class LeagueDB:

    def __init__(self):
        self.league_repository = LeagueRepository()

    def save_account(self, nick_discord, account_instance):
        self.league_repository.save_account(nick_discord, account_instance)

    def get_account(self, nick_discord):
        hash_result = self.league_repository.get_account_by_nick(nick_discord)
        factory_account = FactoryLolAccount(hash_result)
        return factory_account.get_account_lol_instance()

