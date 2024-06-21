from entities.entities_league_of_legends_account.AccountLoL import AccountLoL
from exceptions.league_of_legends_exceptions.InvalidNickNameInput import InvalidNickNameInput
from exceptions.league_of_legends_exceptions.QueueTypeInvalidException import QueueTypeInvalidException
from logger.LoggerConfig import LoggerConfig
from services.league_of_legends_account.external_api.ApiRiotLol import ApiRiot


class LolServices:

    def __init__(self, nick=None, tag=None, queue=None):
        self.tag_line = tag
        self.queue = queue
        self.nick = nick
        self.tag_line = tag
        self.lol_api_services = None
        self.logger = LoggerConfig()

    async def get_league_account(self) -> AccountLoL:
        self.validate_nick_and_tag(self.nick, self.tag_line)
        self.queue = self.extract_queue(self.queue)
        self.logger.get_logger().info("LEAGUE SERVICES: Validating commands inputs")
        self.lol_api_services = ApiRiot(self.nick, self.tag_line, self.queue)
        return await self.lol_api_services.get_all_info_account_league()

    def extract_queue(self, queue_type):
        if queue_type == "solo":
            return "RANKED_SOLO_5x5"
        if queue_type == "flex":
            return "RANKED_FLEX_SR"
        raise QueueTypeInvalidException("Invalid queue!")

    def validate_nick_and_tag(self, nick: str, tag: str):
        if len(nick) < 3 or len(nick) > 16:
            raise InvalidNickNameInput("Nickname length is invalid!")
        if len(tag) < 2 or len(tag) > 5:
            raise InvalidNickNameInput("Tag length is invalid!")
