import unittest

from constants.Contants import TOKEN_RIOT
from exceptions.league_of_legends_exceptions.RiotInvalidNickName import RiotInvalidNickName
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from factory.LolFactory.FactoryAccountLol import FactoryLolAccount
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot


class ApiRioIntegrationTests(unittest.TestCase):
    def test_get_account_entity(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        factory_account_lol = FactoryLolAccount(api_riot_lol.get_all_info_account_league())
        entity_result = factory_account_lol.get_account_lol_instance()
        self.assertEqual("Drikill", entity_result.nick)
        self.assertEqual(402, entity_result.level)
        self.assertEqual("UNRANKED", entity_result.tier)
        self.assertEqual(0, entity_result.winrate)
        self.assertEqual(0, entity_result.pdl)

    def test_get_id_account_by_nick(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        id_account_result = api_riot_lol.get_account_id_by_nick()
        self.assertEqual("VDOzqowJuT3rRD76FfHfuckdsVUIfC7ST70PZB9JVi-51X4",
                         id_account_result)

    def test_level_account(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        level_result = api_riot_lol.get_level_account_by_nick()
        self.assertEqual(402, level_result)

    def test_get_winrate_account_by_nick(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        result_winrate = api_riot_lol.calculate_winrate_account()
        self.assertEqual(0, result_winrate)

    def test_get_tier_account_without_tier(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        result_hash = api_riot_lol.get_all_info_account_league()
        self.assertEqual("UNRANKED", result_hash['tier'])

    def test_get_account_without_win_and_losses_winrate_by_nick(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        result_winrate = api_riot_lol.calculate_winrate_account()
        self.assertEqual(0, result_winrate)

    def test_get_all_account_info(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        hash_info_result = api_riot_lol.get_all_info_account_league()
        self.assertEqual("UNRANKED", hash_info_result['tier'])

    def test_get_all_account_info2(self):
        api_riot_lol = ApiRiot("Raposy#dri", TOKEN_RIOT)
        hash_info_result = api_riot_lol.get_all_info_account_league()
        self.assertEqual("GOLD", hash_info_result['tier'])

    def test_get_all_account_info3(self):
        api_riot_lol = ApiRiot("130722#br1", TOKEN_RIOT)
        hash_info_result = api_riot_lol.get_all_info_account_league()
        self.assertEqual("GOLD", hash_info_result['tier'])

    def test_get_all_account_info4(self):
        api_riot_lol = ApiRiot("Dri#13722", TOKEN_RIOT)
        hash_info_result = api_riot_lol.get_all_info_account_league()
        self.assertEqual("GOLD", hash_info_result['tier'])

    def test_get_id_maestry_champ_by_puuid(self):
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        id_champ_result = api_riot_lol.get_id_best_champion_account_by_puuid_account()
        self.assertEqual(157, id_champ_result)

    def test_get_name_by_champion_id(self):
        ID_CHAMP = 157  # YASUO
        NAME_CHAMP = "Yasuo"
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        id_champ_result = api_riot_lol.get_id_best_champion_account_by_puuid_account()
        self.assertEqual(ID_CHAMP, id_champ_result)
        name_champ_result = api_riot_lol.get_name_by_champion_id()
        self.assertEqual(NAME_CHAMP, name_champ_result)

    def test_get_name_by_champion_id2(self):
        ID_CHAMP = 238
        NAME_CHAMP = "Zed"
        api_riot_lol = ApiRiot("Dri#13722", TOKEN_RIOT)
        id_champ_result = api_riot_lol.get_id_best_champion_account_by_puuid_account()
        self.assertEqual(ID_CHAMP, id_champ_result)
        name_champ_result = api_riot_lol.get_name_by_champion_id()
        self.assertEqual(NAME_CHAMP, name_champ_result)

    def test_get_url_splash_art_by_name_champ(self):
        ID_CHAMP = 157  # YASUO
        NAME_CHAMP = "Yasuo"
        URL_SPLASH_ART = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yasuo_0.jpg"
        api_riot_lol = ApiRiot("Drikill#mel", TOKEN_RIOT)
        id_champ_result = api_riot_lol.get_id_best_champion_account_by_puuid_account()
        self.assertEqual(ID_CHAMP, id_champ_result)
        name_champ_result = api_riot_lol.get_name_by_champion_id()
        self.assertEqual(NAME_CHAMP, name_champ_result)
        url_splash_art_result = api_riot_lol.get_url_splash_art_best_champ_by_id_champ()
        self.assertEqual(URL_SPLASH_ART, url_splash_art_result)

    def test_exception_invalid_token_request(self):
        with self.assertRaises(RiotTokenInvalid):
            ApiRiot("Drikill#mel", "token_errado")

    def test_exception_tag_line_none(self):
        with self.assertRaises(RiotInvalidNickName):
            ApiRiot("Drikill", "token_errado")


if __name__ == '__main__':
    unittest.main()
