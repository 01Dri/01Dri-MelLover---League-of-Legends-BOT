import os
import unittest

from dotenv import load_dotenv

from exceptions.league_of_legends_exceptions.NotFoundAccountRiotException import NotFoundAccountRiotException
from exceptions.league_of_legends_exceptions.QueueTypeInvalidException import QueueTypeInvalidException
from exceptions.league_of_legends_exceptions.RiotInvalidNickName import RiotInvalidNickName
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalidException
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot

load_dotenv()
TOKEN_RIOT = os.getenv("TOKEN_RIOT")
ID_ACCOUNT_DRIKILL = os.getenv("ID_ACCOUNT_TEST")
LEVEL_ACCOUNT_DRIKILL = 407
TIER_ACCOUNT_DRIKILL = "GOLD"
RANK_ACCOUNT_DRIKILL = "III"
LEAGUE_POINTS_ACCOUNT_DRIKILL = 27
WINS_ACCOUNT_DRIKILL = 58
URL_BEST_CHAMO_ACCOUNT_DRIKILL = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yasuo_0.jpg"


class ApiRioIntegrationTests(unittest.TestCase):

    def test_invalid_token(self):
        with self.assertRaises(RiotTokenInvalidException):
            ApiRiot("drikill#mel", "invalido", "RANKED_SOLO_5x5")

    def test_invalid_queue_type(self):
        with self.assertRaises(QueueTypeInvalidException):
            ApiRiot("drikill#mel", TOKEN_RIOT, "queue_nao_existe")

    def test_get_account_id(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_account_id_by_nick()
        self.assertEqual(ID_ACCOUNT_DRIKILL, result)

    def test_get_level_account(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_level_account_by_nick()
        self.assertEqual(LEVEL_ACCOUNT_DRIKILL, result)

    def test_get_tier_account_solo_duo(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_all_info_account_league()  # GET ALL INFO RETURN DICT
        self.assertEqual(TIER_ACCOUNT_DRIKILL, result["tier"])

    def test_get_rank_account_solo_duo(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_all_info_account_league()
        self.assertEqual(RANK_ACCOUNT_DRIKILL, result["rank"])

    def test_get_league_points_account_solo_duo(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_all_info_account_league()
        self.assertEqual(LEAGUE_POINTS_ACCOUNT_DRIKILL, result["lp"])

    def test_get_winrate_account_solo_duo(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_all_info_account_league()
        self.assertEqual(WINS_ACCOUNT_DRIKILL, result["winrate"])

    def test_get_id_best_champ_account(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_id_best_champion_account_by_puuid_account()
        self.assertEqual(157, result)

    def test_get_name_best_champ_account(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        riot_api.get_id_best_champion_account_by_puuid_account()
        result = riot_api.get_name_by_champion_id()
        self.assertEqual("Yasuo", result)

    def test_get_url_best_champ_account(self):
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_SOLO_5x5")
        result = riot_api.get_all_info_account_league()
        self.assertEqual(URL_BEST_CHAMO_ACCOUNT_DRIKILL, result["best_champ_url"])

    def test_get_check_account_without_info_queue_type(self):  # This test verify if account is UNRANKED in specify queue
        # On the case my account "drikill" is UNRANKED in flex queue
        riot_api = ApiRiot("drikill#mel", TOKEN_RIOT, "RANKED_FLEX_SR")
        result = riot_api.get_all_info_account_league()
        self.assertEqual("UNRANKED", result["tier"])
        self.assertEqual("UNRANKED", result["rank"])
        self.assertEqual(0, result["lp"])
        self.assertEqual(0, result["winrate"])

    def test_invalid_nickname_get_account_id(self):
        with self.assertRaises(RiotInvalidNickName) as context:
            ApiRiot("drikill#taginvalida", TOKEN_RIOT, "RANKED_SOLO_5x5")
        self.assertEqual("Tagline is incorrect", str(context.exception))

    def test_not_found_account(self):
        with self.assertRaises(NotFoundAccountRiotException) as context:
            ApiRiot("drikill#13722", TOKEN_RIOT, "RANKED_SOLO_5x5")
        self.assertEqual("Riot account not found", str(context.exception))


if __name__ == '__main__':
    unittest.main()
