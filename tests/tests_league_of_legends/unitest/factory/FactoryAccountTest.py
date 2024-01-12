import unittest
from factory.LolFactory.FactoryAccountLol import FactoryLolAccount

class FactoryAccountTest(unittest.TestCase):

    def test_create_entity(self):
        hash_map_info_account_lol = {
            "id":"4",
            "nick": "Drikill",
            "rank":"IV",
            "tier":"GOLD",
            "winrate":50,
            "pdl":50,
            "op_gg":"teste",
            "best_champ":"Yasuo"
        }

        factory_account_lol = FactoryLolAccount(hash_map_info_account_lol)
        result_entity = factory_account_lol.create_account_lol_entity()
        self.assertEqual("4", result_entity.id)
        self.assertEqual("Drikill", result_entity.nick)
        self.assertEqual("GOLD", result_entity.league)
        self.assertEqual("IV", result_entity.tier)



if __name__ == '__main__':
    unittest.main()
