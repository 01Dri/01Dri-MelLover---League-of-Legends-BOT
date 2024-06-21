class AccountLoL:

    def __init__(self,
                 id=None,
                 puuid=None,
                 nick=None,
                 tag_line=None,
                 level=None,
                 rank=None,
                 tier=None,
                 winrate=None,
                 pdl=None,
                 op_gg=None,
                 best_champ_url=None,
                 best_champ_name=None,
                 wins=None,
                 losses=None,
                 id_best_champ=None,
                 queue_type=None):
        self.id = id
        self.puuid = puuid
        self.nick = nick
        self.tag_line = tag_line
        self.level = level
        self.rank = rank
        self.tier = tier
        self.winrate = winrate
        self.pdl = pdl
        self.op_gg = op_gg
        self.best_champ_url = best_champ_url
        self.best_champ_name = best_champ_url,
        self.id_best_champ = id_best_champ
        
        self.queue_type = queue_type
        self.wins = wins
        self.losses = losses
        