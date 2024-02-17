import random
import unittest

from services.league_of_legends_account.gpt.LeagueAccountGPT import LeagueAccountGPT
from factory.factory import FactoryLolAccount


class LeagueAccountGPTTests(unittest.TestCase):
    def test_gpt_tips_prompt(self):
        gpt = LeagueAccountGPT()
        account_info = {
            'nick': 'Player123',
            'tag_line': 'Victory is ours!',
            'level': random.randint(1, 30),
            'rank': 'Gold',
            'tier': 'III',
            'winrate': random.uniform(40, 70),
            'pdl': random.randint(0, 100),
            'op_gg': 'https://www.op.gg/summoner/userName=Player123',
            'best_champ_url': 'https://www.example.com/champion',
            'queue_type': 'Ranked Solo/Duo'
        }
        factory = FactoryLolAccount(account_info)
        account_lol = factory.get_account_lol_instance()
        result = gpt.get_tips(account_lol)
        print(result)


if __name__ == '__main__':
    unittest.main()
