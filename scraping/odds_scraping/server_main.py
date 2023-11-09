from SiteInteraction import load_webpage, create_driver, create_driver_server, decline_all_cookies
from DataWriter import DataWriter
from HelperFunctions import sleep_randomly

from pyvirtualdisplay import Display
import pyautogui
import json


def main():
    display = Display(visible=0, size=(800, 600))
    display.start()

    # load json data from scraping/odds_scraping/json/countries_links.json
    with open('scraping/odds_scraping/json/countries_links.json') as json_file:
        data = json.load(json_file)
    
    country = 'Europe'
    for league in data[country]:
        league_rows = process_league(data, country, league)
        DataWriter().write_consolidated(league_rows, country, league)
        sleep_randomly(3, 7)

    display.stop()


def process_league(link_dict, country, league):
    current_league = link_dict[country][league]

    driver = create_driver_server()
    writer = DataWriter()
    num_processed = 0

    league_rows = []

    for season in current_league:
        print(f"Loading {country}, {league}, {season}")
        url = current_league[season]

        if num_processed % 5 == 0:
            driver.quit()
            driver = create_driver()
            driver.get(url)
            decline_all_cookies(driver)
        else:
            driver.get(url)

        season_results = load_webpage(driver, url, country, league, season)
        if season_results is None:
            print("Error loading page")
            continue
        league_rows.extend(season_results)
        writer.write_rows(season_results, country, league, season)
        sleep_randomly(0.5, 2)
        num_processed += 1
    
    driver.quit()

    return league_rows
    

main()