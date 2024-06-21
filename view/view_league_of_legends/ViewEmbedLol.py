import discord

from entities.entities_league_of_legends_account.AccountLoL import AccountLoL

COLOR_FOR_EMBEDS = 0x87CEFA
COLOR_FOR_EMBEDS_ERROR = 0xFF0000


def parser_nick_with_space(nick):
    if "%20" in nick:
        return nick.replace("%20", " ").upper()
    return nick.upper()


def parser_nick_char(nick):
    if "%23" in nick:
        return nick.replace("%23", "#").upper()
    return nick.upper()


def get_embed_account_lol(account_lol: AccountLoL):
    nick = parser_nick_with_space(account_lol.nick)
    nick = parser_nick_char(nick)
    embed = discord \
        .Embed(
        title='LEAGUE OF LEGENDS ACCOUNT', description="", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="NICKNAME", value=nick.upper() + "#" + account_lol.tag_line.upper(), inline=False)
    embed.add_field(name="QUEUE", value=account_lol.queue_type, inline=False)
    embed.add_field(name="TIER", value=account_lol.tier + " " + account_lol.rank, inline=False)
    embed.add_field(name="LEVEL", value=account_lol.level, inline=False)
    embed.add_field(name="WINRATE", value=f'{account_lol.winrate}%', inline=False)
    embed.add_field(name="LP", value=account_lol.pdl, inline=False)
    embed.add_field(name="OPGG", value=account_lol.op_gg, inline=False)
    embed.set_image(url=account_lol.best_champ_url)
    return embed


def get_embed_error_get_account_lol(message):
    embed = discord \
        .Embed(
        title='LEAGUE OF LEGENDS ACCOUNT', description="ERROR INFO", color=COLOR_FOR_EMBEDS_ERROR)
    embed.add_field(name=f"Error", value=message,
                    inline=False)
    embed.set_image(url="https://thc.bing.com/th/id/OIG.8PhgK58TGnckz_lgvXvq?pid=ImgGn")  # AI IMAGE
    return embed

def get_embed_account_lol_without_solo_duo_info(account_lol: AccountLoL):
    nick = parser_nick_char(account_lol.nick)
    embed = discord \
        .Embed(
        title='LEAGUE OF LEGENDS ACCOUNT', description="", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="NICKNAME", value=nick.upper() + "#" + account_lol.tag_line.upper(), inline=False)
    embed.add_field(name="QUEUE", value=account_lol.queue_type, inline=False)
    embed.add_field(name="TIER", value="UNRANKED", inline=False)
    embed.add_field(name="LEVEL", value=account_lol.level, inline=False)
    embed.add_field(name="OPGG", value=account_lol.op_gg, inline=False)
    embed.set_image(url=account_lol.best_champ_url)
    return embed


async def get_embed_save_account_on_db(ctx, account_lol: AccountLoL, queue):
    nick = parser_nick_char(account_lol.nick)
    embed = discord \
        .Embed(
        title='LEAGUE OF LEGENDS ACCOUNT', description="", color=COLOR_FOR_EMBEDS)
    embed.add_field(name="Account saved successfully", value=account_lol.nick, inline=False)
    # embed.set_image(url=account_lol.best_champ_url)
    await ctx.reply(embed=embed)


async def get_embed_tips_gpt(ctx, account_lol: AccountLoL, tips):
    nick = parser_nick_char(account_lol.nick)
    embed = discord \
        .Embed(
        title='MEL LOVER - GPT TIPS', description="**ACCOUNT:** " + account_lol.nick + "#" + account_lol.tag_line,
        color=COLOR_FOR_EMBEDS)
    embed.add_field(name="", value=tips, inline=False)
    # embed.set_image(url=account_lol.best_champ_url)
    await ctx.reply(embed=embed)


async def get_embed_error(ctx, message):
    embed = discord \
        .Embed(
        title='LEAGUE OF LEGENDS ACCOUNT', description="ERROR INFO", color=COLOR_FOR_EMBEDS_ERROR)
    embed.add_field(name="Invalid command", value=message,
                    inline=False)
    embed.set_image(url="https://thc.bing.com/th/id/OIG.8PhgK58TGnckz_lgvXvq?pid=ImgGn")  # AI IMAGE
    await ctx.reply(embed=embed)
