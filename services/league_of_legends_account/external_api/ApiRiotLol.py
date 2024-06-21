import asyncio
import os
import re

import aiohttp

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.NotFoundAccountRiotException import NotFoundAccountRiotException
from exceptions.league_of_legends_exceptions.RiotTokenInvalid import RiotTokenInvalidException
from logger.LoggerConfig import LoggerConfig


class ApiRiot:

    def __init__(self, nick, tag, queue) -> None:
        self.token = os.getenv("TOKEN_RIOT")
        self.headers_token = {
            'X-Riot-Token': f'{self.token}'
        }
        self.logger = LoggerConfig()
        self.account_lol = AccountLoL()
        self.nick = nick
        self.tag = tag
        self.queue = queue

    def check_response(self, response):
        invalid_codes = {401, 403}  # INVALID TOKEN OR ERROR OF PERMISSION
        if response.status in invalid_codes:
            self.logger.get_logger_info_error().info(f"Failed to sent request because the token is invalid, status code: {response.status_code}")
            raise RiotTokenInvalidException(
                f"Failed to sent request because the token is invalid, status code: {response.status}")
        if response.status == 404 or response.status == 400:
            self.logger.get_logger_info_error().info(f"Account not found, status code: {response.status}")
            raise NotFoundAccountRiotException("Riot account not found")

    async def get_all_info_account_league(self):
        self.account_lol.queue_type = self.queue
        self.account_lol.nick = self.nick
        self.account_lol.tag_line = self.tag
        await self.update_account()
        return self.account_lol

    async def update_account(self):
        await self.get_account_id_by_nick()
        await self.get_info_queue_account()
        await self.get_level_account_by_nick()
        self.calculate_winrate_account()
        await self.get_url_splash_art_best_champ_by_id_champ()
        self.account_lol.op_gg = f"https://www.op.gg/summoners/br/{self.account_lol.nick}-{self.account_lol.tag_line}"

    async def get_account_id_by_nick(self):
        #  it to can get info about summoner account league, its need to get PUUID first and after get info summoner with this PUUID
        ENDPOINT_GET_PUUID_BY_NICK_AND_TAGLINE = f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{self.nick}/{self.tag}'
        response_api = await self.req(ENDPOINT_GET_PUUID_BY_NICK_AND_TAGLINE)
        self.account_lol.puuid = response_api['puuid']
        ENDPOINT_GET_SUMMONER_ACCOUNT_ID = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.account_lol.puuid}'
        response_api = await self.req(ENDPOINT_GET_SUMMONER_ACCOUNT_ID)
        self.account_lol.id = response_api['id']
        return self.account_lol.id

    async def get_info_queue_account(self):
        endpoint_get_summoner_league_by_id_riot = f'https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.account_lol.id}'
        response_api = await self.req(endpoint_get_summoner_league_by_id_riot)
        print(response_api)
        print(self.account_lol.queue_type)
        if len(response_api) == 0:
            self.set_unranked_field_if_response_is_null()
        else:
            for item in response_api:
                if item.get('queueType') == self.account_lol.queue_type:
                    
                    self.account_lol.tier = item.get('tier')
                    self.account_lol.rank = item.get('rank')
                    self.account_lol.pdl = item.get('leaguePoints')
                    self.account_lol.wins = item.get("wins")
                    self.account_lol.losses = item.get("losses")
        return self

    async def get_level_account_by_nick(self):
        endpoint_get_level_league_by_id_riot = f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.account_lol.puuid}'
        response_api = await self.req(endpoint_get_level_league_by_id_riot)
        self.account_lol.level = response_api['summonerLevel']
        return self.account_lol.level

    def calculate_winrate_account(self):
        try:
            all_games = self.account_lol.wins + self.account_lol.losses
            winrate = (self.account_lol.wins / all_games) * 100
            winrate_round = round(winrate)
            self.account_lol.winrate = winrate_round
            return self.account_lol.winrate
        except ZeroDivisionError:
            self.account_lol.winrate = 0
            return self.account_lol.winrate

    async def get_id_best_champion_account_by_puuid_account(self):
        ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID = f"https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{self.account_lol.puuid}"  ## Get Maestry Champs By Summoner Id was deprecated, now it needs PUUID
        response_api = await self.req(ENDPOINT_GET_ID_CHAMP_RIOT_BY_PUUID)
        champ_max_maestry = max(response_api, key=lambda x: x['championPoints'])
        self.account_lol.id_best_champ = champ_max_maestry['championId']
        return self.account_lol.id_best_champ

    async  def get_name_by_champion_id(self):
        # This endpoint return a JSON with ALL champions of League of Legends
        endpoint_dragon_league_of_legends = "http://ddragon.leagueoflegends.com/cdn/13.17.1/data/en_US/champion.json"
        response_api = await self.req(endpoint_dragon_league_of_legends)
        champions = response_api["data"]
        # This is looking the name of champ in JSON by ID
        champion = next((champ for champ in champions.values() if champ["key"] == str(self.account_lol.id_best_champ)), None)
        self.account_lol.best_champ_name = champion["name"]
        return self.account_lol.best_champ_name

    async def get_url_splash_art_best_champ_by_id_champ(self):
        await self.get_id_best_champion_account_by_puuid_account()
        await self.get_name_by_champion_id()
        self.account_lol.best_champ_name = re.sub(r'\s', '', self.account_lol.best_champ_name)  # Removing spaces of the name

        # This endpoint return ALL splash arts of champs from league of legends by NAME Of champ
        self.account_lol.best_champ_url = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{self.account_lol.best_champ_name}_0.jpg"
        return self.account_lol.best_champ_url

    def set_unranked_field_if_response_is_null(self):
        self.account_lol.tier = "UNRANKED"
        self.account_lol.winrate = "UNRANKED"
        self.account_lol.pdl = 0
        self.account_lol.wins = 0
        self.account_lol.losses = 0
        return self
    
    async def req(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=self.headers_token) as response:
                self.check_response(response)
                return await response.json()
        
        