from sqlalchemy.orm import Session

from entities.entities_league_of_legends_account.data.LeagueAccount import LeagueAccount


class LeagueRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_account_by_nick_discord(self, nick_discord: str):
        return self.db.query(LeagueAccount).filter(LeagueAccount.nick_discord == nick_discord).first()

    def create_account(self, account: LeagueAccount):
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def remove_account_by_discord_name(self, discord_name: str):
        self.db.query(LeagueAccount).filter(LeagueAccount.nick_discord == discord_name).delete()
        self.db.commit()
