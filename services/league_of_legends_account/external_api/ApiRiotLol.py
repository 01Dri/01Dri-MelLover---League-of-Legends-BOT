import re

import requests

from exceptions.league_of_legends_exceptions.NotFoundAccountRiotException import NotFoundAccountRiotException
from exceptions.league_of_legends_exceptions.RiotResponseError import RiotResponseError
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalidException
from logger.LoggerConfig import LoggerConfig


class ApiRiot:

    def __init__(self, nick,tag_line,  token, queue_type) -> None:
        self.token = token
        self.headers_token = {
            'X-Riot-Token': f'{self.token}'
        }
        self.logger = LoggerConfig()
        self.nick = nick
        self.tag_line = tag_line
        self.id_account = None
        self.puuid = None
        self.rank = None
        self.tier = None
        self.pdl = None
        self.level = None
        self.wins = 0
        self.losses = 0
        self.winrate = None
        self.id_best_champion = None
        self.nick_name_best_champ = None
        self.url_splash_art_best_champ = None
        self.json_http_response_riot = None
        self.queue_type = queue_type
        self.get_account_id_by_nick()

    def check_response(self, response):
        invalid_codes = {401, 403}  # INVALID TOKEN OR ERROR OF PERMISSION
        if response.status_code == 200:
            self.json_http_response_riot = response.json()
            return
        if response.status_code in invalid_codes:
            self.logger.get_logger_info_error().info(f"Failed to sent request because the token is invalid, status code: {response.status_code}")
            raise RiotTokenInvalidException(
                f"Failed to sent request because the token is invalid, status code: {response.status_code}")
        if response.status_code == 404 or response.status_code == 400:
            self.logger.get_logger_info_error().info(f"Account not found, status code: {response.status_code}")
            raise NotFoundAccountRiotException("Riot account not found")
        self.logger.get_logger_info_error().info(f"Error riot response, status code: {response.status_code}")
        raise RiotResponseError(
            f"Error in riot response, status: {response.status_code}")

    def get_all_info_account_league(self):
        self.update_account()
        op_gg_account = f"https://www.op.gg/summoners/br/{self.nick}-{self.tag_line}"
        hash_map_info = {'id': self.id_account, 'nick': self.nick, 'tag_line':self.tag_line, 'tier': self.tier, 'rank': self.rank,
                         'lp': self.pdl, 'level': self.level, 'winrate': self.winrate,
                         'op_gg': op_gg_account, 'best_champ_url': self.get_url_splash_art_best_champ_by_id_champ(), 'queue_type':self.queue_type}
        return hash_map_info

    def update_account(self):
        self.get_info_queue_account(self.queue_type)
        self.get_level_account_by_nick()
        self.calculate_winrate_account()

    def get_account_id_by_nick(self):
        #  it to can get info about summoner account league, its need to get PUUID first and after get info summoner with this PUUID
        ENDPOINT_GET_PUUID_BY_NICK_AND_TAGLINE = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.nick}/{self.tag_line}'
        response_api = requests.get(ENDPOINT_GET_PUUID_BY_NICK_AND_TAGLINE, headers=self.headers_token)
        self.check_response(response_api)
        self.puuid = self.json_http_response_riot['puuid']
        ENDPOINT_GET_SUMMONER_ACCOUNT_ID = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}'
        response_api = requests.get(ENDPOINT_GET_SUMMONER_ACCOUNT_ID, headers=self.headers_token)
        self.check_response(response_api)
        self.id_account = self.json_http_response_riot['id']
        return self.id_account

    def get_info_queue_account(self, queue_type):
        endpoint_get_summoner_league_by_id_riot = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}'
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        self.check_response(response_api)
        for item in self.json_http_response_riot:
            if item.get('queueType') == queue_type:
                self.tier = item.get('tier')
                self.rank = item.get('rank')
                self.pdl = item.get('leaguePoints')
                self.wins = item.get("wins")
                self.losses = item.get("losses")
            else:
                self.set_unranked_field_if_response_is_null()
        return self

    def get_level_account_by_nick(self):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        self.check_response(response_api)
        self.level = self.json_http_response_riot['summonerLevel']
        return self.level

    def calculate_winrate_account(self):
        try:
            all_games = self.wins + self.losses
            winrate = (self.wins / all_games) * 100
            winrate_round = round(winrate)
            self.winrate = winrate_round
            return self.winrate
        except ZeroDivisionError:
            self.winrate = 0
            return self.winrate

    def get_id_best_champion_account_by_puuid_account(self):
        ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.puuid}"  ## Get Maestry Champs By Summoner Id was deprecated, now it needs PUUID
        response_api = requests.get(ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID, headers=self.headers_token)
        self.check_response(response_api)
        champ_max_maestry = max(self.json_http_response_riot, key=lambda x: x['championPoints'])
        self.id_best_champion = champ_max_maestry['championId']
        return self.id_best_champion

    def get_name_by_champion_id(self):
        # This endpoint return a JSON with ALL champions of League of Legends
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        response_api = requests.get(endpoint_dragon_league_of_legends)
        self.check_response(response_api)
        champions = self.json_http_response_riot["data"]
        # This is looking the name of champ in JSON by ID
        champion = next((champ for champ in champions.values() if champ["key"] == str(self.id_best_champion)), None)
        self.nick_name_best_champ = champion["name"]
        return self.nick_name_best_champ

    def get_url_splash_art_best_champ_by_id_champ(self):
        self.get_id_best_champion_account_by_puuid_account()
        self.get_name_by_champion_id()
        self.nick_name_best_champ = re.sub(r'\s', '', self.nick_name_best_champ)  # Removing spaces of the name

        # This endpoint return ALL splash arts of champs from league of legends by NAME Of champ
        self.url_splash_art_best_champ = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{self.nick_name_best_champ}_0.jpg"
        return self.url_splash_art_best_champ

    def set_unranked_field_if_response_is_null(self):
        self.tier = "UNRANKED"
        self.rank = "UNRANKED"
        self.pdl = 0
        self.wins = 0
        self.losses = 0
        return self
