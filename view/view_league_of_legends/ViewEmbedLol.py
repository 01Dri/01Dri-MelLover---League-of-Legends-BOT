import discord

from constants.Contants import COLOR_FOR_EMBEDS
from constants.Contants import COLOR_FOR_EMBEDS_ERROR


def parser_nick_with_space(nick):
    if "%20" in nick:
        return nick.replace("%20", " ").upper()
    return nick.upper()


def parser_nick_char(nick):
    if "%23" in nick:
        return nick.replace("%23", "#").upper()
    return nick.upper()


class ViewEmbedLol:

    def __init__(self):
        pass

    async def get_embed_account_lol(self, ctx, nick, league, tier, level, winrate, pdl, op_gg, url_splash_art_champ):
        nick = parser_nick_with_space(nick)
        nick = parser_nick_char(nick)
        embed = discord \
            .Embed(
            title='LEAGUE OF LEGENDS ACCOUNT', description="SOLO DUO QUEUE", color=COLOR_FOR_EMBEDS)
        embed.add_field(name="NICKNAME", value=nick.upper(), inline=False)
        embed.add_field(name="TIER", value=tier + " " + league, inline=False)
        embed.add_field(name="LEVEL", value=level, inline=False)
        embed.add_field(name="WINRATE", value=f'{winrate}%', inline=False)
        embed.add_field(name="LP", value=pdl, inline=False)
        embed.add_field(name="OPGG", value=op_gg, inline=False)
        embed.set_image(url=url_splash_art_champ)
        await ctx.reply(embed=embed)

    async def get_embed_error_get_account_lol(self, ctx, message):
        embed = discord \
            .Embed(
            title='LEAGUE OF LEGENDS ACCOUNT', description="ERROR INFO", color=COLOR_FOR_EMBEDS_ERROR)
        embed.add_field(name=f"Conta não encontrada!!!", value=message,
                        inline=False)
        embed.set_image(url="https://thc.bing.com/th/id/OIG.8PhgK58TGnckz_lgvXvq?pid=ImgGn")  # AI IMAGE
        await ctx.reply(embed=embed)

    async def get_embed_account_lol_without_solo_duo_info(self, ctx, nick, level, op_gg, url_splash_art_champ):
        nick = parser_nick_char(nick)
        embed = discord \
            .Embed(
            title='LEAGUE OF LEGENDS ACCOUNT', description="SOLO DUO QUEUE", color=COLOR_FOR_EMBEDS)
        embed.add_field(name="NICKNAME", value=nick.upper(), inline=False)
        embed.add_field(name="TIER", value="UNRANKED", inline=False)
        embed.add_field(name="LEVEL", value=level, inline=False)
        embed.add_field(name="OPGG", value=op_gg, inline=False)
        embed.set_image(url=url_splash_art_champ)
        await ctx.reply(embed=embed)
