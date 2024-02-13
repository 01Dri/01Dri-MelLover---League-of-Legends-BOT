import unittest

from factory.FactoryAccountLol import FactoryLolAccount
from repositories.league_repository.LeagueRepository import LeagueRepository


class LeagueRepositoryTest(unittest.TestCase):
    def test_save_account(self):
        account_lol_info = {
            'id': "sdasjdakj",
            'nick': "Diego",
            'level': 450,
            'rank': '3',
            'tier': "GOLD",
            'winrate': 50,
            'lp': 70,
            'op_gg': "testge.com.br",
            'best_champ': "Yasuo"
        }
        account_factory = FactoryLolAccount(account_lol_info)
        account_lol_instance = account_factory.get_account_lol_instance()
        repository = LeagueRepository()
        repository.save_account(account_lol_instance)

    def test_get_account(self):
        repository = LeagueRepository()
        result = repository.get_account_by_nick("Diego")
        self.assertEqual("Diego", result['nick'])
        self.assertEqual("3", result['league'])
        self.assertEqual("GOLD", result['tier'])
        self.assertEqual(450, result['levle'])
        self.assertEqual(50, result['winrate'])
        self.assertEqual(70, result['lp'])
        self.assertEqual("testge.com.br", result['op_gg'])
        self.assertEqual("Yasuo", result['best_champ'])
if __name__ == '__main__':
    unittest.main()


