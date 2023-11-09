from bs4 import BeautifulSoup

class ResultsReader:
    MONTH_DICTIONARY = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }

    def __init__(self):
        self.date_selector = '.text-black-main.font-main.w-full.truncate.text-xs.font-normal.leading-5'
        self.match_row_selector = '.border-black-borders.group.flex.border-l.border-r.hover\\:bg-\\[\\#f9e9cc\\]'


    def read_page(self, page_source, country_name, league_name, year):
        # select this class with bs4: flex flex-col px-3 text-sm max-mm:px-0
        soup = BeautifulSoup(page_source, 'html.parser')
        table_wrapper = soup.select_one('.flex.flex-col.px-3.text-sm.max-mm\\:px-0')
        if table_wrapper is None:
            print("No table wrapper found.")
            return None

        event_rows = table_wrapper.find_all('div', class_='eventRow')

        page_results = []
        date = ''
        for row in event_rows:
            if row.select_one(self.date_selector):
                date_split = row.select_one(self.date_selector).text.strip().split(" ")
                date = f"{date_split[0]}-{date_split[1]}-{date_split[2]}"

            match_row = row.select_one(self.match_row_selector)
            if match_row:
                data = self.process_match_row(match_row, country_name, league_name, year, date)
                page_results.append(data)
        
        print(f"Processed {len(page_results)} rows")
        return page_results


    def process_match_row(self, match_row, country_name, league_name, year, date):
        match_row_data = [child for child in match_row.children if child.name == 'div']
        if match_row_data is None or len(match_row_data) < 4:
            print("No valid match row data found")
            return None
        
        game_results = self.extract_match_data(match_row_data[0])
        if game_results is None:
            print("No valid game results found")
            return None

        home_odds = match_row_data[1].text.strip()
        draw_odds = match_row_data[2].text.strip()
        away_odds = match_row_data[3].text.strip()

        if (home_odds != '-' and draw_odds != '-' and away_odds != '-'):
            implied_home = round(1 / float(home_odds), 4)
            implied_draw = round(1 / float(draw_odds), 4)
            implied_away = round(1 / float(away_odds), 4)
        else:
            implied_home = 0
            implied_draw = 0
            implied_away = 0

        final_results = [
            country_name, league_name, year, date, game_results["time"], 
            game_results["home_team"], game_results["away_team"], 
            game_results["home_score"], game_results["away_score"],
            home_odds, draw_odds, away_odds,
            implied_home, implied_draw, implied_away
        ]
        return final_results


    def extract_match_data(self, game_results):
        # Extract time
        time_element = game_results.find('p')
        time_text = time_element.text.strip()

        # Extract team names and scores
        teams = game_results.select('.participant-name')
        team_names = [team.text.strip() for team in teams]

        scores = game_results.select('.font-bold')

        score_values = [score.text.strip() for score in scores if score.text.strip().isdigit()]
        if len(score_values) == 3:
            score_values = [int(score_values[0]), int(score_values[2])]
        else:
            score_values = [0, 0]

        return {
            "time": time_text,
            "home_team": team_names[0],
            "away_team": team_names[1],
            "home_score": score_values[0],
            "away_score": score_values[1]
        }