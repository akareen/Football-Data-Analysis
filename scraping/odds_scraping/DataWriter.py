import csv, os

class DataWriter:

    ODDS_HEADERS = [
        "country_name", "league_name", "year", "date", "time", 
        "home_team", "away_team", "home_score", "away_score", 
        "home_odds", "draw_odds", "away_odds", 
        "implied_home", "implied_draw", "implied_away"
    ]


    def __init__(self, data_storage_location='odds_data'):
        self.data_storage_location = data_storage_location
        if not os.path.exists(data_storage_location):
            os.makedirs(data_storage_location)


    def write_data(self, data, country_name, league_name):
        if data is None:
            return

        country_storage = f"{self.data_storage_location}/{country_name}"
        if not os.path.exists(country_storage):
            os.makedirs(country_storage)

        filename = f"{country_storage}/{country_name}_{league_name}.csv"
        
        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.ODDS_HEADERS)
                writer.writerows(data)
        else:
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
