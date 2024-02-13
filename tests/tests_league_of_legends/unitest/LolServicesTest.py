import unittest

from services.league_of_legends_account.LolServices import LolServices


class LolServicesTest(unittest.TestCase):

    def test_fetch_inputs(self):
        lol_services = LolServices("!accountlol-solo drikill#mel")
        self.assertEqual("drikill", lol_services.nick)


if __name__ == '__main__':
    unittest.main()
