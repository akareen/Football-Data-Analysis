import json, csv, os, time

from HelperFunctions import api_get_soup

class ByYearScrape:
    
    def __init__(self, seasons_data_json_link: str, league_display_name: str, data_storage_path="match_and_player_data/competition_data"):
        self.seasons_data = self.load_seasons_data(seasons_data_json_link)[league_display_name]
        self.data_storage_path = data_storage_path

        self.seasons_data_path = data_storage_path + "/" + league_display_name
        self.match_report_storage_path = '/'.join(seasons_data_json_link.split("/")[:-1]) + "/match_reports_links.json"

        with open(self.match_report_storage_path, 'r') as f:
            self.match_reports = json.load(f)

        self.league_display_name = league_display_name

        sorted_keys = sorted(
            self.seasons_data,
            key=lambda x: int(x.split('-')[-1]),  # This takes the last year from a range if it exists
            reverse=True
        )
        self.league_link_name, self.base_url = self.get_league_base_url(self.seasons_data[sorted_keys[0]])


    def load_seasons_data(self, json_link: str) -> dict:
        with open(json_link, 'r') as f:
            seasons_data = json.load(f)
        return seasons_data


    def get_league_base_url(self, orig_url: str) -> str:
        # Format is like: https://fbref.com/en/comps/9/Premier-League-Stats
        split_url = orig_url.split('/')

        base_split = split_url[2:6]
        base_url = 'https://' + '/'.join(base_split)

        league_link_name = split_url[-1].rstrip('-Stats')

        return league_link_name, base_url



    def scrape_scores(self) -> None:
        total = 95
        i = 0
        for season_year in self.seasons_data:
            if (season_year == '1921-1922'):
                i += 1
                continue
            if i < total:
                i += 1
                continue
            print(f"Processing {season_year}...")
            season_link = self.seasons_data[season_year]
            self.scrape_season(season_link, season_year)
            print(f"Finished processing {season_year}...")


        with open(self.match_report_storage_path, 'w') as f:
            json.dump(self.match_reports, f, indent=4)


    def scrape_season(self, season_link: str, season_year: str) -> None:
        # Scraping all of the League Overview page

        # Scraping basic Scores and Fixtures data
        basic_score_data, match_report_urls = self.scrape_basic_scores(season_year)
        self.write_basic_score_data(basic_score_data, season_year)
        self.write_to_dict(self.match_reports, self.league_display_name, season_year, match_report_urls)

        # Scraping all Match Reports

        # Scraping all Squad and Player data in aggregate

        # Scraping Player data for each match
        pass


    def scrape_basic_scores(self, season_year: str) -> None:
        # Format = https://fbref.com/en/comps/9/1906-1907/schedule/1906-1907-Premier-League-Scores-and-Fixtures
        score_reports_url = f"{self.base_url}/{season_year}/schedule/{season_year}-{self.league_link_name}-Scores-and-Fixtures"
        soup = api_get_soup(score_reports_url)
        match_report_urls = []

        score_table_container = soup.find('div', {'id': 'all_sched'})
        if not score_table_container:
            time.sleep(123)
            soup = api_get_soup(score_reports_url)
            score_table_container = soup.find('div', {'id': 'all_sched'})
        score_table = score_table_container.find('tbody')
        score_rows = score_table.find_all(lambda tag: tag.name == 'tr' and not tag.get('class'))
        
        day_info = {"gameweek": '', "date": '', "dayofweek": ''}
        all_score_data = []
        
        for score_row in score_rows:
            score_row_data = []
            for data_point in score_row.find_all(['th', 'td']):
                data_point_label = data_point.get('data-stat')
                if data_point in day_info:
                    if data_point.text:
                        day_info[data_point_label] = data_point.text
                    score_row_data.append(day_info[data_point_label])
                elif data_point_label == 'match_report':
                    link = data_point.find('a')
                    match_report_urls.append("https://fbref.com" + link.get('href') if link else '')
                elif data_point_label == 'score':
                    split_score = data_point.find('a').text.split('–')
                    score_row_data.append(split_score[0])
                    score_row_data.append(split_score[1])
                else:
                    score_row_data.append(data_point.text)

            all_score_data.append(score_row_data)

        return all_score_data, match_report_urls

        
    def write_basic_score_data(self, basic_score_data: list, season_year: str) -> None:
        year_storage_path = f"{self.seasons_data_path}/{season_year}"
        os.makedirs(year_storage_path, exist_ok=True)

        score_data_headers = [
            "Week", "Day", "Date", "Time", "Home Team", 
            "Home Expected Goals", "Home Goals", "Away Goals", 
            "Away Expected Goals", "Away Team", 
            "Attendance", "Venue", "Referee", "Match Report", "Notes"
        ]
        with open(f"{year_storage_path}/{season_year}_SCORE_DATA.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(score_data_headers)
            writer.writerows(basic_score_data)


    def write_to_dict(self, data: dict, league_name: str, season_year: str, data_to_write: list) -> None:
        if league_name not in data:
            data[league_name] = {}
        if season_year not in data[league_name]:
            data[league_name][season_year] = []
        data[league_name][season_year] = data_to_write


if __name__ == "__main__":
    scraper = ByYearScrape("main_scraping/json/season_links.json", "Premier League")
    scraper.scrape_scores()