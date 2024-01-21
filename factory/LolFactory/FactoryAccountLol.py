from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.ErrorGetValueHashMapInfoAccount import ErrorGetValueHashMapInfoAccount


class FactoryLolAccount:

    def __init__(self, hash_map_info_account_lo):
        self.info_account = hash_map_info_account_lo
        pass

    def get_account_lol_instance(self):
        try:
            id_account = self.info_account['id']
            nick = self.info_account['nick']
            level = self.info_account['level']
            rank = self.info_account['rank']
            tier = self.info_account['tier']
            winrate = self.info_account['winrate']
            pdl = self.info_account['pdl']
            op_gg = self.info_account['op_gg']
            best_champ_url = self.info_account['best_champ']
            return AccountLoL(id_account, nick, level, rank, tier, winrate, pdl, op_gg, best_champ_url)
        except KeyError as e:
            raise ErrorGetValueHashMapInfoAccount(f"ERROR WHILE GET VALUES OF HASH MAP WITH INFO ACCOUNT LEAGUE: {e}")
