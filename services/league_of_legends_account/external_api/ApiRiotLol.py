import re
import requests
from exceptions.league_of_legends_exceptions.RiotInvalidNickName import RiotInvalidNickName
from exceptions.league_of_legends_exceptions.RiotResponseError import RiotResponseError
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalid
from logger.LoggerConfig import LoggerConfig


class ApiRiot:

    def __init__(self, nick, token) -> None:
        self.token = token
        self.headers_token = {
            'X-Riot-Token': f'{self.token}'
        }
        self.logger = LoggerConfig()
        self.nick = nick
        self.tag_line = None
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
        self.parse_nick_tag_line()
        self.get_account_id_by_nick()

    def check_response(self, response):
        response_json = response.json()
        self.json_http_response_riot = response_json
        if response.status_code != 200:
            http_status_response = response_json['status']
            error_message_response = http_status_response['message']
            LOG_ERROR_RIOT_MESSAGE = f'RIOT RESPONSE, STATUS: {http_status_response}, ERROR MESSAGE {error_message_response}'
            self.logger.get_logger_info_error().error(LOG_ERROR_RIOT_MESSAGE)
            invalid_codes = {400, 401, 403} # INVALID TOKEN OR ERROR OF PERMISSION
            if response.status_code in invalid_codes:
                raise RiotTokenInvalid(
                    f"Failed to sent request because the token is invalid, status code: {response.status_code} and error message: {error_message_response}")
            raise RiotResponseError(
                f"Error in riot response, status: {http_status_response}, error message: {error_message_response}")

    ## This method make a calling of functions to set values on attributes
    def get_all_info_account_league(self):
        self.get_account_tier_rank_pdl_win_losses_by_id_account()
        op_gg_account = f"https://www.op.gg/summoners/br/{self.nick}-{self.tag_line}"
        self.get_level_account_by_nick()
        self.calculate_winrate_account()
        hash_map_info = {'id': self.id_account, 'nick': self.nick, 'tier': self.tier, 'rank': self.rank,
                         'pdl': self.pdl, 'level': self.level, 'winrate': self.winrate,
                         'op_gg': op_gg_account, 'best_champ': self.get_url_splash_art_best_champ_by_id_champ()}
        return hash_map_info

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

    def get_account_tier_rank_pdl_win_losses_by_id_account(self):
        endpoint_get_summoner_league_by_id_riot = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}'
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        self.check_response(response_api)
        if not self.json_http_response_riot:
            self.set_unranked_field_if_response_is_null()  # The player of league of legends may not have info about ranked queues, then it to set 'UNRANKED' in fields
        for item in self.json_http_response_riot:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                self.tier = item.get('tier')
                self.rank = item.get('rank')
                self.pdl = item.get('leaguePoints')
                self.wins = item.get("wins")
                self.losses = item.get("losses")
                break
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

    ## This function is used to remove the '#' character of command !contalol <nick>#<tag_line>
    def parse_nick_tag_line(self):
        nick_splited_porcent = self.nick.split("%23")
        if len(nick_splited_porcent) > 1:
            self.nick = nick_splited_porcent[0]
            self.tag_line = nick_splited_porcent[1]
            return self

        nick_splited_hash = self.nick.split("#")
        if len(nick_splited_hash) > 1:
            self.nick = nick_splited_hash[0]
            self.tag_line = nick_splited_hash[1]
            return self
        raise RiotInvalidNickName('Tagline is None')
