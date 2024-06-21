from sqlalchemy.orm import Session

from entities.entities_league_of_legends_account.data.LeagueAccount import LeagueAccount
from repositories.league_repository.LeagueRepository import LeagueRepository
from repositories.league_repository.databaseconfig import engine, SessionLocal
from entities.entities_league_of_legends_account.AccountLoL import AccountLoL


#Session SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LeagueServicesDB:

    def __init__(self):
        LeagueAccount.metadata.create_all(bind=engine)
        db: Session = next(get_db())
        self.repo = LeagueRepository(db)

    def save_account(self, account_lol: AccountLoL, discord_name):
        leagueaccount = self.convert_account_to_league_account(account_lol, discord_name)
        self.repo.create_account(leagueaccount)

    def remove_account_by_discord_name(self, discord_name: str):
        self.repo.remove_account_by_discord_name(discord_name)

    def get_account_by_discord_name(self, nick_discord):
        account_lol = self.repo.get_account_by_nick_discord(nick_discord)
        if account_lol is not None:
            return self.convert_league_account_to_account(account_lol)
        return account_lol

    def convert_league_account_to_account(self, league_account: LeagueAccount):
        return AccountLoL(
            nick=league_account.nick_game,
            tag_line=league_account.tag_line,
            level=league_account.level,
            rank=league_account.rank,
            tier=league_account.tier,
            winrate=league_account.winrate,
            pdl=league_account.lp,
            op_gg=league_account.op_gg,
            best_champ_url=league_account.best_champ_url,
            wins=league_account.wins,
            losses=league_account.losses,
            queue_type=league_account.queue_type
        )

    def convert_account_to_league_account(self, account_lol: AccountLoL, discord_nick: str):
        return LeagueAccount(
            nick_discord=discord_nick,
            nick_game=account_lol.nick,
            rank=account_lol.rank,
            level=account_lol.level,
            winrate=account_lol.winrate,
            lp=account_lol.pdl,
            op_gg=account_lol.op_gg,
            best_champ_url=account_lol.best_champ_url,
            queue_type=account_lol.queue_type,
            tag_line=account_lol.tag_line,
            tier=account_lol.tier,
            wins=account_lol.wins,
            losses=account_lol.losses

        )
