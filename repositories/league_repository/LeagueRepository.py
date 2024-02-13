import sqlite3

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.FailedToSaveAccountInDatabaseException import FailedToSaveAccountInDatabase


class LeagueRepository:

    def __init__(self):
        self.con = None
        self.cur = None
        pass

    def get_account_by_nick(self, nick_discord):
        self.con = sqlite3.connect("/home/dridev/Desktop/MelLover2.0/repositories/league_repository/LEAGUE_ACCOUNT.db")
        self.cur = self.con.cursor()
        res = self.cur.execute("SELECT * FROM LEAGUE_ACCOUNT WHERE nick_discord = ?", (str(nick_discord),))
        result_info = res.fetchall()  # Fetchall return a List of result with tuples inside
        result_tuple = result_info[0]  # It to getting first result of list
        self.cur.close()
        self.con.close()
        return self.get_hash_result(result_tuple)

    def save_account(self, nick_discord, instance_account: AccountLoL):
        try:
            self.con = sqlite3.connect(
                "/home/dridev/Desktop/MelLover2.0/repositories/league_repository/LEAGUE_ACCOUNT.db")
            self.cur = self.con.cursor()
            self.cur.execute("SELECT COUNT(*) FROM LEAGUE_ACCOUNT WHERE nick_discord = ?", (str(nick_discord),))
            result = self.cur.fetchone()[0]
            print(result)
            if result > 0:
                self.update_account(instance_account, nick_discord)
                return True
            self.insert_account(instance_account, nick_discord)
            return True
        except Exception as e:
            raise FailedToSaveAccountInDatabase(e)

    ## This function is getting values of a tuple and to putting into a hash
    def get_hash_result(self, result_tuple):
        hash_result = {
            'nick': result_tuple[1],
            'rank': result_tuple[3],
            'tier': result_tuple[4],
            'level': result_tuple[5],
            'winrate': result_tuple[6],
            'lp': result_tuple[7],
            'op_gg': result_tuple[8],
            'best_champ_url': result_tuple[9]
        }
        return hash_result

    def insert_account(self, instance_account, nick_discord):
        self.cur.execute(
            "INSERT INTO LEAGUE_ACCOUNT (nick, nick_discord, league, tier, level, winrate, lp, best_champ, "
            "op_gg) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                instance_account.nick,
                str(nick_discord),
                instance_account.league,
                instance_account.tier, instance_account.level,
                instance_account.winrate, instance_account.pdl,
                instance_account.best_champ_url, instance_account.op_gg))
        self.con.commit()
        self.cur.close()
        self.con.close()

    def update_account(self, instance_account, nick_discord):
        self.cur.execute(
            "UPDATE LEAGUE_ACCOUNT SET nick = ?, league = ?, tier = ?, level = ?, winrate = ?, lp = ?, best_champ = "
            "?, op_gg = ? WHERE nick_discord = ?",
            (
                instance_account.nick,
                instance_account.league,
                instance_account.tier,
                instance_account.level,
                instance_account.winrate,
                instance_account.pdl,
                instance_account.best_champ_url,
                instance_account.op_gg,
                str(nick_discord)
            )
        )
        self.con.commit()
        self.cur.close()
        self.con.close()
