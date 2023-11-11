# ⚽️ Football Data Analysis
![Football Data Analysis Banner Image](/assets/readme_banner.png)
<div align="center">
  <img src="https://img.shields.io/github/last-commit/akareen/Football-Data-Analysis">
  <img src="https://img.shields.io/github/contributors/akareen/Football-Data-Analysis">
  <img src="https://img.shields.io/github/stars/akareen/Football-Data-Analysis?style=social">
  <img src="https://img.shields.io/github/forks/akareen/Football-Data-Analysis?style=social">
</div>
<br>
An in-depth analysis of Football data for all major leagues. The aim is for this repository to contain comprehensive data, tools and code for exploring and analysing Football match and player statistics, as well as historical odds data.  

This project is currently under development, to see a repository that this is being based on, please see my repostitory [AFL-Data-Analysis](https://github.com/akareen/AFL-Data-Analysis).

I am currently making progress on the scraping and cleaning of the data, there is a variety of sources that are detailed in some areas whilst lacking in others so I am working on making the data as consistent as possible.

## Table of Contents
- [🔦 Overview](#overview)
  - [🛠 Features](#features)
- [💾 Installation](#installation)
  - [📖 Usage](#usage)
  - [🔍 Scraping Examples](#scraping-examples)
- [📚 Odds Data Guide](#odds-data-guide)
- [📚 Data Guide](#data-guide)
- [🔗 Data Sources](#data-sources)
- [🤝 Contributing](#contributing)
- [⚖️ License](#license)

## 🔦 Overview

The Football Data Analysis project provides a comprehensive platform for examining and deriving insights from Football odds, match and player data. Whether you're a sports enthusiast, a tipper, a data scientist, or a student, this repository offers valuable resources for diving into the world of Football.

To ensure that the scraping scripts remain up-to-date, I will be updating them regularly to ensure that they are working as intended. They will not be published as the sites have been difficult to crack and sharing the code here will likely result in the sites being updated to prevent scraping. If you would like to use the scripts, please contact me and I will be happy to share them with you.

A sampling of match and player data can be found in the **match_and_player_data** folder, the data from the Premier League is a small sample of the data that will be available in the future. The link to it is [here](/match_and_player_data/competition_data/ALL_MATCH_RESULTS.csv)

The historical odds data for 1,303 leagues is available in the **odds_data** folder, the link to it is [here](/odds_data)

Contributions are encouraged; don't hesitate to submit a pull request or contact me with the details on my GitHub profile.


### 🛠 Features

**Current Offerings:**
- Data on the leagues of 173 countries worldwide and 1,303 leagues in total
- More than 1.1 million rows of unique data. Odds data was the most difficult to scrape as it would not permit headless scraping, so this is a major achievement.
- The most comprehensive downloadable source of historical odds data. Allowing for complete backtesting.
- Cleansed data, primed for analysis
- Extracted links for all matches, players and teams. Which will be used to scrape more data in the future.

**In the Pipeline (timeline to completion = by the end of November):**
- Extracting the detailed result data for every worldwide league
- Extracting the detailed player data that has played in any league. An example of the detail I want for each player can be seen in my repository [AFL-Data-Analysis](https://github.com/akareen/AFL-Data-Analysis).
- Extracting the detailed team data for every worldwide league
- Storing the data in both CSV and JSON format for ease of use


**Future Plans:**
- Dedicated database system
- Advanced scoring algorithms
- Visualization tools for performance metrics
- Machine learning models for predicting match, player and team performance
- Backtesting of the machine learning models to accurately judge the likelihood for teams to win

**Suggestions?**
- Pitch in your wishlist. One current suggestion: Player GPS Data

## 💾 Installation

You can either download the data directly from from GitHub or clone the repository to your local machine (this allows for updates). The data is stored in CSV format, so it can be opened in any spreadsheet software.

Clone the repository:
```bash
git clone https://github.com/akareen/Football-Data-Analysis.git
```


### 📖 Usage

### 🔍 Scraping Examples

## 📚 Odds Data Guide

The odds data is organised with the following structure:
```
country_name
└── league_name
    └── season
        └── {country_name}_{league_name}_{season}.csv
    └── {country_name}_{league_name}_COMPREHENSIVE.csv
```

All folder names and file names are uppercase and spaces between parts use underscores, spaces within names are replaced with hyphens. The COMPREHENSIVE file contains all of the data for that league, the other files are split into seasons.

The odds data is currently stored in CSV format to keep it lightweight, it will be stored in a database in the future. As Selenium GUI scraping requiring human-like automation was required it took roughly 40 hours for the scraping scripts to run. In light of that more detailed odds such as Asian Handicap and Over/Under will be added in the future, as it would require a factor of 20 times more scraping time as that data is not on the main page but in each matches link. Scraping through requests and reading the JSON data would be much faster, but the sites have been designed to prevent this.

A sampling of the data can be seen below:
![Match Data Example](/assets/odds_data_example.png)

The following headers are used for the data (all snakecase):
```
'country_name', 'league_name', 'year', 'date', 'time', 'home_team', 'away_team', 'home_score', 'away_score', 'home_odds', 'draw_odds', 'away_odds', 'implied_home', 'implied_draw', 'implied_away'
```

## 📚 Data Guide

## 🔗 Data Sources

## 🤝 Contributing

Football Data Analysis thrives on collaboration! Got a novel analysis idea or data source? Open an issue or send a pull request. Your expertise is invaluable in elevating this project.

## ⚖️ License

Football Data Analysis is under the MIT License. Refer to the [LICENSE](LICENSE) file for a complete understanding.