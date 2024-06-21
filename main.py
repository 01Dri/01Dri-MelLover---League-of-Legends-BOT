import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from logger.LoggerConfig import LoggerConfig

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=".", intents=intents)


async def load_commands():
    await bot.wait_until_ready()
    await bot.load_extension("cogs.accountlolcogs")
@bot.command()
async def async_commands (ctx:commands.Context):
    await load_commands()
    sincs = await bot.tree.sync()
    await ctx.reply(f"{len(sincs)} sincronizados")
    
    
@bot.event
async def on_ready():
    await load_commands()
    await bot.tree.sync()
    config_logger = LoggerConfig()
    config_logger.config_logger_level(logging.INFO)
    logger = config_logger.get_logger()
    logger.info(f"STATING BOT {bot.user}")


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN_DISCORD"))
