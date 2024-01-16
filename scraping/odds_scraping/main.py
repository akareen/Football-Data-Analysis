from SiteInteraction import create_driver, extract_league_links, extract_page_data
from DataWriter import DataWriter
from HelperFunctions import sleep_randomly
from ObjectMaker import update_object
import json


def scrape_update():
    """
    This code is used to update the data. It will scrape the data from the
    last scraped date up to the current date. It will also update the last
    scraped date in the link_data.json file.
    """
    # If there are any new leagues, add them to the link_data.json file
    update_object(
        input_location='scraping/odds_scraping/json/link_data.json', 
        output_location='scraping/odds_scraping/json/link_data.json')

    # The data will be in the format {country: {league: {url: url, last_scraped_date: date}, ....}, ....}
    with open('scraping/odds_scraping/json/link_data.json') as json_file:
        data = json.load(json_file)
    
    for country in data:
        if country < 'PORTUGAL':
            continue
        driver = create_driver()
        for league in data[country]:
            current_league_data = data[country][league]              
            data_to_append = process_league(driver, country, league, current_league_data)

            if data_to_append and len(data_to_append) > 0:
                DataWriter().write_data(data_to_append, country, league)

            sleep_randomly(0.3, 1) # Sleep between 0.3 and 1 seconds
        
        driver.quit()

        # Do it for each country to prevent data loss in the case of crashes
        with open('scraping/odds_scraping/json/link_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)


def process_league(driver, country: str, league: str, current_league_data: dict) -> list:
    """
    This function will scrape the data from the last scraped date up to the current date.
    It will also update the last scraped date in the countries_links.json file.
    params:
        driver: The webdriver object
        country: The country name
        league: The league name
        current_league_data: The current league data
    return:
        league_rows: The list of rows to append to the CSV file
    """
    url = current_league_data['url']
    last_scraped_date = current_league_data['last_scraped_date']

    # Extracting the season links and names from the league page
    url_links, season_names = extract_league_links(url)
    league_rows = []
    new_last_scraped = ''
    
    for url, season in zip(url_links, season_names):
        driver.get(url)
        
        season_results, more_data_to_extract, last_date_reached = extract_page_data(
            driver, url, country, league, season, last_scraped_date)
        league_rows.extend(season_results)
        
        if new_last_scraped == '':
            new_last_scraped = last_date_reached

        if not more_data_to_extract:
            break
        sleep_randomly(0.15, 0.25)

    # Updating the last scraped date
    current_league_data['last_scraped_date'] = new_last_scraped
    return league_rows[::-1] # Returning the list in ascending order, earliest date first
    

if __name__ == "__main__":
    scrape_update()