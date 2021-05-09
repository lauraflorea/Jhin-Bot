import discord
from config import images_path

def make_simple_embed(title, msg) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.red()
    )

    embed.add_field(name=title, value=msg, inline=True)

    return embed

def make_top_champs_embed(top, role, champs) -> discord.Embed:
    embed = discord.Embed(
        color=discord.Color.dark_red()
    )

    embed.set_author(name=f'Top {top} champs for {role.capitalize()}:')

    champ_dict = {'ranks': "", 'names': "", 'win rate': ""}

    for c in champs:
        champ_dict['ranks'] += f'{c.get_rank()}\n'
        champ_dict['names'] += f'{c.get_name()}\n'
        champ_dict['win rate'] += f'{c.get_win_rate()}\n'

    embed.add_field(name='Rank', value=champ_dict['ranks'], inline=True)
    embed.add_field(name='Name', value=champ_dict['names'], inline=True)
    embed.add_field(name='Win Rate', value=champ_dict['win rate'], inline=True)

    return embed

def make_champ_embed(champ):
    embed = discord.Embed(
        color=discord.Color.gold()
    )

    embed.set_author(name=f'Champion info for {champ.get_name()}:')

    embed.add_field(name='Roles', value="\n".join(champ.get_roles()), inline=True)
    embed.add_field(name='Win Rate', value="\n".join(champ.get_win_rate()), inline=True)
    embed.add_field(name='Pick Rate', value="\n".join(champ.get_pick_rate()), inline=True)

    file = discord.File(f'{images_path}{champ.get_image_name()}', filename=champ.get_image_name())
    embed.set_thumbnail(url=f'attachment://{champ.get_image_name()}')

    return file, embed

def help_embed():
    embed = discord.Embed(
        color=discord.Color.orange()
    )

    embed.set_author(name='Jhin Bot Help Page:')

    commands = {
        '4!test': 'Test command to see if Jhin Bot is alive.',
        '4!quote': 'Returns a random signature Jhin quote.',
        "4!best-champs [role] ['', '5', '10', 'all']": 'Returns the best champs for a particular role. Requires role '
                                                       'and number of champs to display if the user wants to display '
                                                       'more than the top 5.',
        '4!get-stats [champion name]': 'Gets statistics for all of a champion\'s roles. Requires champion name.',
    }

    for cmd in commands:
        embed.add_field(name=cmd, value=commands[cmd], inline=False)

    return embed
