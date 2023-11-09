import random, time
from selenium.webdriver.common.action_chains import ActionChains
import json, requests
from bs4 import BeautifulSoup
from Config import get_soup


def api_get_soup(link):
    api_key = '2e34fdfdabd81b5855103af3ddd69909'
    payload = { 'api_key': api_key, 'url': link }
    r = requests.get('https://api.scraperapi.com/', params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


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


def sleep_randomly(start_seconds, end_seconds):
    # Use a normal distribution for sleep time with truncation to make it more human-like.
    mean_sleep_time = (start_seconds + end_seconds) / 2
    stddev = (end_seconds - start_seconds) / 4  # std dev is 1/4 the range to keep most sleep times within bounds
    sleep_time = max(start_seconds, min(end_seconds, random.gauss(mean_sleep_time, stddev)))
    time.sleep(sleep_time)


def perform_random_actions(driver, num_actions=10):
    for _ in range(num_actions):
        action = random.choice(['scroll', 'keypress'])
        
        if action == 'scroll':
            # Scroll a random amount in a random direction
            scroll_amount = random.randint(-300, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        
        elif action == 'keypress':
            # Press a random letter key
            key_to_press = random.choice('abcdefghijklmnopqrstuvwxyz')
            ActionChains(driver).send_keys(key_to_press).perform()