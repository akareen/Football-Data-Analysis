import json
from LeaguesScraping import LeaguesScraping

def main():
    LeaguesScraping().scrapeLeagues()

    with open ("main_scraping/json/season_links.json", 'r') as f:
        season_links = json.load(f)

    print(season_links)

    pass

if __name__ == "__main__":
    main()