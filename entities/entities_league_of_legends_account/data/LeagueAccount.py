from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LeagueAccount(Base):
    __tablename__ = 'league_account'
    id = Column(Integer, primary_key=True)
    nick_discord = Column(String, nullable=False)
    nick_game = Column(String, nullable=False)
    rank = Column(String, nullable=True)
    tier = Column(String, nullable=True)
    level = Column(Integer, nullable=False)
    winrate = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    lp = Column(Integer, nullable=True)
    op_gg = Column(String, nullable=False)
    best_champ_url = Column(String, nullable=False)
    queue_type = Column(String, nullable=False)
    tag_line = Column(String, nullable=False)
