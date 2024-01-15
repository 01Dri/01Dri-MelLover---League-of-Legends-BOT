import requests

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
        self.id_account = self.get_account_id_by_nick()

    def validation_token(self, response):
        self.logger.get_logger_info_level().info("VALIDATING TOKEN BY RESPONSE STATUS CODE")
        if response.status_code == 403 or response.status_code == 401:
            response_json = response.json()
            http_status_response = response_json['status']
            error_message_response = http_status_response['message']
            self.logger.get_logger_info_error().error(
                f'TOKEN INVALID STATUS: {http_status_response} ERROR MESSAGE: {error_message_response}')
            raise RiotTokenInvalid(
                f"Failed to sent request because the token is invalid, status code: {response.status_code} and error message: {error_message_response}")

    def verify_status_code_request(self, response):
        if response.status_code != 200:
            response_json = response.json()
            http_status_response = response_json['status']
            error_message_response = http_status_response['message']
            self.logger.get_logger_info_error().error(
                f'ERROR API RESPONSE RIOT, STATUS CODE: {http_status_response} ERROR MESSAGE: {error_message_response}')
            raise RiotResponseError(
                f'Error in riot response, status code: {http_status_response}, and error message: {error_message_response}')

    def get_all_info_account_league(self):
        self.get_account_id_by_nick()
        self.get_account_tier_rank_and_pdl()
        op_gg_account = f"https://www.op.gg/summoners/br/{self.nick}"
        self.get_level_account_by_nick()
        self.get_winrate_account_by_nick()
        hash_map_info = {'id': self.id_account, 'nick': self.nick, 'tier': self.tier, 'rank': self.rank,
                         'pdl': self.pdl, 'level': self.level, 'winrate': self.winrate,
                         'op_gg': op_gg_account, 'best_champ': self.get_url_splash_art_best_champ_by_id_champ()}
        return hash_map_info

    def get_account_id_by_nick(self):
        endpoint_get_summoner_by_nick_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.nick}'
        response_api = requests.get(endpoint_get_summoner_by_nick_riot, headers=self.headers_token)
        self.validation_token(response_api)
        self.verify_status_code_request(response_api)
        response_api_json = response_api.json()
        self.id_account = response_api_json['id']
        self.puuid = response_api_json['puuid']  # ID ALTERNATIVE RIOT ACCOUNT
        return self.id_account

    def get_account_tier_rank_and_pdl(self):
        endpoint_get_summoner_league_by_id_riot = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}'
        print(endpoint_get_summoner_league_by_id_riot)
        response_api = requests.get(endpoint_get_summoner_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        self.verify_status_code_request(response_api)
        response_api_json = response_api.json()
        print(response_api_json)
        for item in response_api_json:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                self.tier = item.get('tier')
                self.rank = item.get('rank')
                self.pdl = item.get('leaguePoints')
                break
        print(self.tier)

    def get_level_account_by_nick(self):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{self.nick}'
        response_api = requests.get(endpoint_get_level_league_by_id_riot, headers=self.headers_token)
        self.validation_token(response_api)
        self.verify_status_code_request(response_api)
        response_api_json = response_api.json()
        self.level = response_api_json['summonerLevel']
        return self.level

    def get_winrate_account_by_nick(self):
        API_ENDPOINT_RIOT_LEAGUE = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.id_account}'
        response_api = requests.get(API_ENDPOINT_RIOT_LEAGUE, headers=self.headers_token)
        self.validation_token(response_api)
        self.verify_status_code_request(response_api)
        response_api_json = response_api.json()
        self.get_wins_and_losses(response_api_json)
        all_games = self.wins + self.losses
        try:
            winrate = (self.wins / all_games) * 100
            winrate_round = round(winrate)
            self.winrate = winrate_round
            return self.winrate
        except ZeroDivisionError:
            self.winrate = 0
            return self.winrate


    def get_wins_and_losses(self, response_api):
        for item in response_api:
            if item.get("queueType") == "RANKED_SOLO_5x5":
                self.wins = item.get("wins")
                self.losses = item.get("losses")
                break
        return self

    def get_id_best_champion_account_by_puuid(self):
        ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.puuid}"  ## Get Maestry Champs By Summoner Id was deprecated, now it needs PUUID
        response_api = requests.get(ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID, headers=self.headers_token)
        self.validation_token(response_api)
        self.verify_status_code_request(response_api)
        response_api_json = response_api.json()
        champ_max_maestry = max(response_api_json, key=lambda x: x['championPoints'])
        id_champ_max = champ_max_maestry['championId']
        self.id_best_champion = id_champ_max
        return id_champ_max

    def get_name_by_champion_id(self):
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        response_api = requests.get(endpoint_dragon_league_of_legends)
        self.verify_status_code_request(response_api)
        data = response_api.json()
        champions = data["data"]
        champion = next((champ for champ in champions.values() if champ["key"] == str(self.id_best_champion)), None)
        champion_name = champion["name"]
        self.nick_name_best_champ = champion_name
        return champion_name

    def get_url_splash_art_best_champ_by_id_champ(self):
        self.get_id_best_champion_account_by_puuid()
        self.get_name_by_champion_id()
        url_image_champ_splash = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{self.nick_name_best_champ}_0.jpg"
        self.url_splash_art_best_champ = url_image_champ_splash
        return url_image_champ_splash
