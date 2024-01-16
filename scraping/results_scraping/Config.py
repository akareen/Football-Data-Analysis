from unidecode import unidecode


MAX_RETRIES = 5
DELAY_BETWEEN_REQUESTS = 5  # 5 seconds, adjust as needed
INITIAL_DELAY = 1

CONFIG = {
    # User-agents to avoid being blocked by the website
    "USER_AGENTS": [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36 OPR/54.0.2952.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36 QIHU 360SE'
    ],

    "MONTH_DICTIONARY": {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    },

    # Headers for the CSV file
    "CSV_HEADERS": [
        "Country", "League", "Season", "Date", "Kick Off (GMT)", 
        "Home Team", "Away Team", "Home Score", "Away Score", 
        "Result (H/D/A)", "Home Odds", "Draw Odds", "Away Odds"
    ]
}

def name_format(name):
    name = unidecode(name)
    formatted_name = name.strip().replace(" ", '-')
    formatted_name = formatted_name.replace('/', '-')
    while '--' in formatted_name:
        formatted_name = formatted_name.replace('--', '-')
    return formatted_name.upper()