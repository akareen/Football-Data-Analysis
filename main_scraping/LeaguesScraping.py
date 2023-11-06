from HelperFunctions import get_all_comp_links, api_get_soup
import json, requests


class LeaguesScraping:
    
    def __init__(self, base_url="https://fbref.com"):
        self.league_links = self.load_league_links()
        self.base_url = base_url


    def load_league_links(self, json_filename="main_scraping/json/competition_links.json") -> dict:
        get_all_comp_links(destination=json_filename)
        league_links = {}

        with open(json_filename, 'r') as f:
            league_links = json.load(f)
        return league_links


    def get_links_of_seasons(self, league_links: dict) -> dict:
        links_for_seasons = {}

        for league in league_links:
            link = league_links[league]
            print(f"Processing {league}, {link}")

            soup = api_get_soup(link)

            # soup = get_soup(link)
            links_for_seasons[league] = {}

            table = soup.find('table', {'id': 'seasons'})
            if table is None:
                continue

            table_body = table.find('tbody')
            
            for row in table_body.find_all('tr', {'class': None}):
                # year_link is the th with 'data-stat' = 'year_id'
                year_info = row.find('th', {'data-stat': 'year_id'})
                if year_info is None:
                    year_info = row.find('th', {'data-stat': 'year'})
                year_link = self.base_url + year_info.find('a').get('href')
                year_name = year_info.text
                links_for_seasons[league][year_name] = year_link
        
        return links_for_seasons

    def scrapeLeagues(self):
        league_links = self.load_league_links()

        
        links_for_seasons = self.get_links_of_seasons(league_links)

        with open("main_scraping/json/season_links.json", 'w') as f:
            json.dump(links_for_seasons, f, indent=4)