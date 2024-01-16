from ProxyScraper import ProxyScraper
import re


def get_location_dictionaries(soup):
    home_players = soup.find_all("div", class_="poptip a")
    away_players = soup.find_all("div", class_="poptip b")

    results = {'home': get_players(home_players), 'away': get_players(away_players)}
    return results


def get_players(player_divs):
    players = {}
    for player in player_divs:
        name = player.get('title')
        style = player.get('style')
        top, left = extract_position(style)
        players[name] = {'top': top, 'left': left}
    return players


def extract_position(style):
    regex = r"top: calc\((\d+\.?\d*)%.*?\);.*?(left|right): calc\((\d+\.?\d*)%"
    matches = re.findall(regex, style)

    if matches:
        top, side, value = matches[0]
        value = float(value)
        
        if side == 'right':
            value = 100 - value

        return round(float(top), 2), round(value, 2)
    else:
        return "No matches found"


def extract_player_positions():
    url = 'https://fbref.com/en/matches/a35e1792/Cyprus-Lithuania-November-19-2023-Friendlies-M'
    scraper = ProxyScraper('scraping/results_scraping/webshare_proxies.txt')
    soup = scraper.get_soup_with_proxy(url)
    return get_location_dictionaries(soup)

players = extract_player_positions()
print(players)