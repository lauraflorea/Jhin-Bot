import re
import requests

from bs4 import BeautifulSoup

import config
from champion import Champion

def get_champ_info(role, top):
    """
    A function which gets the required information for the specified number of champions in a certain role.
    :param role: str
    :param top: str
    :return: Champion List
    """

    if top.lower() not in config.num_champs_req:
        return []

    r = requests.get(config.url)
    soup = BeautifulSoup(r.text, 'html.parser')

    role = soup.find('tbody', class_=f'tabItem champion-trend-tier-{role.upper()}')
    champ_soup = role.find_all('tr')

    champs = create_champ_list(champ_soup)

    if top.lower() == 'all':
        return champs
    else:
        return champs[:int(top)]

def create_champ_list(champ_soup):
    """
    A function which creates all of the required Champion objects and returns them in a list.
    :param champ_soup: bs4.element.Tag List
    :return: Champion List
    """

    champs = []

    for c in champ_soup:
        champs.append(create_champ(c))

    return champs

def create_champ(c):
    """
    A function which parses the information for a champion and creates and returns a new Champion object using it.
    :param c: bs4.element.Tag
    :return: Champion
    """

    fields = c.find_all('td')
    fields = [f.text.strip() for f in fields]

    champ_info = fields[3].split('\n\n')
    champ_info[1] = re.findall('[a-z]+', champ_info[1], flags=re.IGNORECASE)

    champ = Champion(
        name=champ_info[0],
        roles=champ_info[1],
        rank=fields[0],
        win_rate=fields[4],
        pick_rate=fields[5]
    )

    return champ

def get_champ(name):
    """
    A function which gets all of the information for a particular champion in all of their roles and returns it as a
    Champion object.
    :param name: str
    :return: Champion
    """

    champ_roles = []
    win_rates = []
    pick_rates = []

    for r in config.roles:
        champs = get_champ_info(r, 'all')

        for c in champs:
            if c.get_name() == name:
                champ_roles.append(r.capitalize())
                win_rates.append(c.get_win_rate())
                pick_rates.append(c.get_pick_rate())

    if len(win_rates) == 0:
        return None

    champ = Champion(name, champ_roles, 0, win_rates, pick_rates)

    return champ
