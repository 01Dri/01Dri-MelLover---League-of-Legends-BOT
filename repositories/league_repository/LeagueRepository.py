import sqlite3

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.repositories.FailedToSaveAccountInDatabaseException import FailedToSaveAccountInDatabase


class LeagueRepository:

    def __init__(self):
        self.con = None
        self.cur = None
        pass

    def get_account_by_nick(self, nick):
        self.con = sqlite3.connect("/home/dridev/Desktop/MelLover2.0/repositories/league_repository/LEAGUE_ACCOUNT.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT * FROM LEAGUE_ACCOUNT WHERE nick = ?", (nick,))
        result_info = res.fetchall()  # Fetchall return a List of result with tuples inside
        result_tuple = result_info[0]  # It to getting first result of list
        self.cur.close()
        self.con.close()
        return self.get_hash_result(result_tuple)

    def save_account(self, instance_account: AccountLoL):
        try:
            self.con = sqlite3.connect(
                "/home/dridev/Desktop/MelLover2.0/repositories/league_repository/LEAGUE_ACCOUNT.db")
            self.cur = self.con.cursor()
            self.cur.execute(
                "INSERT INTO LEAGUE_ACCOUNT (nick, league, tier, levle, winrate, lp, best_champ, op_gg) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    instance_account.nick, instance_account.league,
                    instance_account.tier, instance_account.level,
                    instance_account.winrate, instance_account.pdl,
                    instance_account.best_champ, instance_account.op_gg))
            self.con.commit()
            self.cur.close()
            self.con.close()
            return True
        except Exception as e:
            raise FailedToSaveAccountInDatabase(e)

    ## This function is getting values of a tuple and to putting into a hash
    def get_hash_result(self, result_tuple):
        hash_result = {
            'nick': result_tuple[1],
            'league': result_tuple[2],
            'tier': result_tuple[3],
            'levle': result_tuple[4],
            'winrate': result_tuple[5],
            'lp': result_tuple[6],
            'op_gg': result_tuple[7],
            'best_champ': result_tuple[8]
        }
        return hash_result
