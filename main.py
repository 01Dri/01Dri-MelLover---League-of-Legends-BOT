import logging
import os
import discord
from controller.Commands import BotCommands
from dotenv import load_dotenv
from logger.LoggerConfig import LoggerConfig

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    config_logger = LoggerConfig()
    config_logger.config_logger_level(logging.INFO)
    logger = config_logger.get_logger()
    logger.info(f"STATING BOT {client.user}")


@client.event
async def on_message(message):
    handler_commands = BotCommands(client)
    await handler_commands.handler_commands(message)


if __name__ == "__main__":
    client.run(os.getenv("TOKEN_DISCORD"))
