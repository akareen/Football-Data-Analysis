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


    def write_rows(self, data, country_name, league_name, year):
        filename = self.make_file_name(country_name, league_name, year)
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.ODDS_HEADERS)
            writer.writerows(data)


    def write_consolidated(self, data, country_name, league_name):
        country_name = country_name.replace(" ", "-").upper()
        league_name = league_name.replace(" ", "-").upper()
        filename = f"{self.data_storage_location}/{country_name}/{league_name}/{country_name}_{league_name}_CONSOLIDATED.csv"

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.ODDS_HEADERS)
            writer.writerows(data)


    def make_file_name(self, country_name, league_name, year):
        country_name = country_name.replace(" ", "-").upper()
        league_name = league_name.replace(" ", "-").upper()
        year = year.replace("/", "-")

        subfolder = f"{self.data_storage_location}/{country_name}/{league_name}"
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        return f"{subfolder}/{country_name}_{league_name}_{year}.csv"