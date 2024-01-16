from Config import get_soup
import json
from unidecode import unidecode

def get_all_comp_links(url="https://fbref.com/en/comps/", destination="main_scraping/json/competition_links.json"):
    base_url = "https://fbref.com"

    soup = get_soup(url)

    league_links = {}

    for th in soup.find_all('th', {'data-stat': 'league_name'}):
        a_tag = th.find('a')
        if a_tag:
            link = base_url + a_tag.get('href')
            text = a_tag.text
            league_links[text] = link

    with open(destination, 'w') as f:
        json.dump(league_links, f, indent=4)


def name_format(name):
    name = unidecode(name)
    return name.strip().replace("-", '').replace(" ", '-').upper()
