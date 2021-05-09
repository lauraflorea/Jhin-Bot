import os

from random import randint
from discord.ext import commands
from dotenv import load_dotenv

import config
import embeds

from scrape import get_champ_info, get_champ


def check_role(role):
    """
    A function which checks if the role the user wants to search for is valid.
    :param role: str
    :return: bool
    """

    if role.upper() not in config.roles:
        return False

    return True


def get_quote():
    """
    A function which randomly chooses a Jhin quote and returns it.
    :return: str
    """

    with open(config.quotes_path) as f:
        lines = f.readlines()

    i = randint(0, len(lines) - 1)

    return lines[i]


class JhinBot(commands.Bot):
    def __init__(self, command_prefix, help_command, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, help_command=help_command, self_bot=self_bot)
        self.add_bot_commands()

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')

    def add_bot_commands(self):
        @self.command(name='test', pass_context=True)
        async def test(ctx):
            """A function which sends a message to the user that the bot is alive."""

            msg = "I'm alive, how lovely!"
            embed = embeds.make_simple_embed('Jhin Bot\'s status:', msg)

            await ctx.send(embed=embed)

        @self.command(name='quote')
        async def quote(ctx):
            """A function which returns a random Jhin quote."""

            msg = get_quote()
            embed = embeds.make_simple_embed('Jhin Bot\'s selected quote:', msg)

            await ctx.send(embed=embed)

        @self.command(name='best-champs')
        async def top_champs(ctx, role='', top='5'):
            """A function which returns the best champs for the role of the user's choosing."""

            champ_role = check_role(role)

            if not champ_role:
                msg = "The role you entered is invalid. Please use 'top', 'jungle', 'mid', 'adc', " "or 'support'."
                await ctx.send(embed=embeds.make_simple_embed('Error:', msg))

            champs = get_champ_info(role, top)

            if not champs:
                msg = "The number of champions you desire to display is invalid. Please use '5', '10', or 'all'."
                await ctx.send(embed=embeds.make_simple_embed('Error:', msg))

            embed = embeds.make_top_champs_embed(top, role, champs)

            await ctx.send(embed=embed)

        @self.command(name='get-stats')
        async def get_stats(ctx, *name_words):
            """A function which returns the stats for a champion of the user's choosing."""

            if not name_words:
                msg = "You have not entered a champion name."
                await ctx.send(embed=embeds.make_simple_embed('Error:', msg))

            name = " ".join(name_words)  # Need to join together args, some champions have multiple word names.
            champ = get_champ(name)

            if not champ:
                msg = "You have either spelt the champion name wrong or op.gg does not have enough data for that " \
                      "champion. Please try again."
                await ctx.send(embed=embeds.make_simple_embed('Error:', msg))

            champ_embed = embeds.make_champ_embed(champ)

            await ctx.send(file=champ_embed[0], embed=champ_embed[1])

        @self.command(name='help')
        async def bot_help(ctx):
            """A function which returns the help information for the bot to the user."""

            embed = embeds.help_embed()

            await ctx.send(embed=embed)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = JhinBot(command_prefix='4!', help_command=None, self_bot=False)

bot.run(TOKEN)
