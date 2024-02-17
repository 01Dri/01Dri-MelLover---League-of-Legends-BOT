import os
import re
import traceback
import urllib.parse

from dotenv import load_dotenv

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.InvalidNickNameInput import InvalidNickNameInput
from exceptions.league_of_legends_exceptions.NotFoundAccountRiotException import NotFoundAccountRiotException
from exceptions.league_of_legends_exceptions.RiotResponseError import RiotResponseError
from factory.factory import FactoryLolAccount
from logger.LoggerConfig import LoggerConfig
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot
from view.view_league_of_legends.ViewEmbedLol import get_embed_account_lol, get_embed_error_get_account_lol, \
    get_embed_account_lol_without_solo_duo_info, get_embed_error


class LolServices:

    def __init__(self, ctx, content):
        self.nick = None
        self.tag_line = None
        self.queue = None
        self.ctx = ctx
        self.content_command_message = content
        self.lol_api_services = None
        self.logger = LoggerConfig()
        load_dotenv()
        self.TOKEN_RIOT = os.getenv("TOKEN_RIOT")

    async def get_league_account(self):
        self.logger.get_logger().info("LEAGUE SERVICES: Validating commands inputs")
        await self.fetch_inputs()
        try:
            self.lol_api_services = ApiRiot(self.nick, self.tag_line, self.TOKEN_RIOT, self.queue)
        except NotFoundAccountRiotException as e:
            await get_embed_error_get_account_lol(self.ctx,
                                                  f"**This username:** {self.nick}" + "#" + f"{self.tag_line} **is invalid!!!**")
            self.logger.get_logger().exception(f"Exception NotFoundAccountRiotException: {e}\n{traceback.format_exc()}")

        self.logger.get_logger().info("LEAGUE SERVICES: Waiting API RIOT response")
        factory_account = FactoryLolAccount(self.lol_api_services.get_all_info_account_league())
        try:
            account_lol: AccountLoL = factory_account.get_account_lol_instance()
            await self.send_embeds_discord_message(self.ctx, account_lol)
            self.logger.get_logger().info("LEAGUE SERVICES: Command successfully, displaying result to user")
            return account_lol
        except RiotResponseError as e:
            await get_embed_error_get_account_lol(self.ctx, f"An error has occurred")
            self.logger.get_logger().exception(f"Exception RiotResponseError: {e}\n{traceback.format_exc()}")

    async def send_embeds_discord_message(self, ctx, entity_account: AccountLoL):
        if entity_account.tier == "UNRANKED":
            await get_embed_account_lol_without_solo_duo_info(ctx, entity_account, self.queue)
        await get_embed_account_lol(ctx, entity_account)

    async def fetch_inputs(self):
        await self.extract_nick_and_tag_line()
        self.queue = await self.extract_queue()

    async def extract_nick_from_command(self):
        parts = self.content_command_message.split()
        if len(parts) > 1:
            full_nick = urllib.parse.quote(" ".join(parts[1:]))
            return full_nick
        self.logger.get_logger().error(f"LEAGUE SERVICES: Invalid nickname: {self.content_command_message}")
        await get_embed_error(self.ctx, "Nick doesn't can be none")
        raise InvalidNickNameInput("Nick doesn't can be none")

    async def extract_queue(self):
        pattern = r'!accountlol-(.*?)\s'
        match_regex = re.search(pattern, self.content_command_message)
        if match_regex:
            if match_regex.group(1) == "solo":
                return "RANKED_SOLO_5x5"
            if match_regex.group(1) == "flex":
                return "RANKED_FLEX_SR"
            self.logger.get_logger().error(f"LEAGUE SERVICES: Invalid nickname: {self.content_command_message}")
            await get_embed_error(self.ctx, "Invalid queue, try !accountlol-solo or flex <nick>")
            raise InvalidNickNameInput("Queue doesn't can be none")
        self.logger.get_logger().error(f"LEAGUE SERVICES: Invalid nickname: {self.content_command_message}")
        await get_embed_error(self.ctx, "Queue doesn't ca be none, try !accountlol-solo or flex <nick>")
        raise InvalidNickNameInput("Queue doesn't can be none")

    async def extract_nick_and_tag_line(self):
        full_nick = await self.extract_nick_from_command()
        nick_splited_porcent = full_nick.split("%23")
        if len(nick_splited_porcent) > 1:
            temp_nick = nick_splited_porcent[0]
            temp_tag_line = nick_splited_porcent[1]
            if temp_nick != "" or len(temp_tag_line) <= 5 or self.tag_line != "":
                self.nick = temp_nick
                temp_tag_line = temp_tag_line.split("%")
                self.tag_line = temp_tag_line[0]
                return
            self.logger.get_logger().error(f"LEAGUE SERVICES: Invalid nickname: {self.content_command_message}")
            await get_embed_error(self.ctx, f"Invalid nickname")
            raise InvalidNickNameInput(f"Invalid nickname")

        self.logger.get_logger().error(f"LEAGUE SERVICES: Invalid nickname: {self.content_command_message}")
        await get_embed_error(self.ctx, f"Please report '#' tag line")
        raise InvalidNickNameInput("Tag line is none")
