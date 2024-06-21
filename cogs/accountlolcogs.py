import discord
from discord import app_commands
from discord.ext import commands

from services.league_of_legends_account.LeagueServicesDB import LeagueServicesDB
from services.league_of_legends_account.LolServices import LolServices
from view.view_league_of_legends.ViewEmbedLol import get_embed_account_lol, get_embed_account_lol_without_solo_duo_info, \
    get_embed_error_get_account_lol

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL


class AccountLoLCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.lol_services = LolServices()
        self.lol_services_db = LeagueServicesDB()
        self.accountlol = None

    @app_commands.command(name="accountlol")
    async def accountlol(self, interact: discord.Interaction, nick: str, tag: str, queue: str):
        self.lol_services.nick = nick
        self.lol_services.tag_line = tag
        self.lol_services.queue = queue
        try:
            await interact.response.send_message("Searching account...", ephemeral=True)
            accountlol = await self.lol_services.get_league_account()
            if accountlol.tier is None or accountlol.rank is None:
                return await interact.followup.send(embed=get_embed_account_lol_without_solo_duo_info(accountlol))
            await interact.followup.send(embed=get_embed_account_lol(accountlol))
        except Exception as e:
            await interact.followup.send(embed=get_embed_error_get_account_lol(e))

    @app_commands.command()
    async def accountlolsaved(self, interact: discord.Interaction):
        await interact.response.send_message("Searching your account saved...", ephemeral=True)
        discord_name = interact.user.name
        accountlol = self.lol_services_db.get_account_by_discord_name(discord_name)
        if accountlol is not None:
            if accountlol.rank is None or accountlol.tier is None:
                return await interact.followup.send(content=f"Account: **{accountlol.nick}** found!", embed=get_embed_account_lol_without_solo_duo_info(accountlol))
            return await interact.followup.send(embed=get_embed_account_lol(accountlol))
        await interact.followup.send("You don't have any account saved", ephemeral=True)

    @app_commands.command()
    async def accountlolremove(self, interact: discord.Interaction):
        discord_name = interact.user.name
        if self.lol_services_db.get_account_by_discord_name(discord_name):
            self.lol_services_db.remove_account_by_discord_name(discord_name)
            return await interact.response.send_message("Account removed", ephemeral=True)
        else:
            return await interact.response.send_message("You don't have any account saved!", ephemeral=True)

    @app_commands.command()
    async def accountlolsave(self, interact: discord.Interaction, nick: str, tag: str, queue: str):
        await interact.response.send_message("Saving account...", ephemeral=True)
        self.lol_services.nick = nick
        self.lol_services.tag_line = tag
        self.lol_services.queue = queue
        discord_name = interact.user.name
        try:
            accountlol: AccountLoL = await self.lol_services.get_league_account()
            self.lol_services_db.save_account(accountlol, discord_name)
            if accountlol.rank is None or accountlol.tier is None:
                return await interact.followup.send(embed=get_embed_account_lol_without_solo_duo_info(accountlol))
            await interact.followup.send(embed=get_embed_account_lol(accountlol))
        except Exception as e:
            await interact.followup.send(embed=get_embed_error_get_account_lol(e), ephemeral=True)


async def setup(bot):
    await bot.add_cog(AccountLoLCommands(bot))
