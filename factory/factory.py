from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.ErrorGetValueHashMapInfoAccount import ErrorGetValueHashMapInfoAccount


class FactoryLolAccount:

    def __init__(self, hash_map_info_account_lo):
        self.info_account = hash_map_info_account_lo

    def get_account_lol_instance(self):
        try:
            nick = self.info_account['nick']
            tag_line = self.info_account['tag_line']
            level = self.info_account['level']
            rank = self.info_account['rank']
            tier = self.info_account['tier']
            winrate = self.info_account['winrate']
            pdl = self.info_account['lp']
            op_gg = self.info_account['op_gg']
            best_champ_url = self.info_account['best_champ_url']
            queue_type = self.info_account['queue_type']
            return AccountLoL(nick,tag_line, level, rank, tier, winrate, pdl, op_gg, best_champ_url, queue_type)
        except KeyError as e:
            raise ErrorGetValueHashMapInfoAccount(f"ERROR WHILE GET VALUES OF HASH MAP WITH INFO ACCOUNT LEAGUE: {e}")
