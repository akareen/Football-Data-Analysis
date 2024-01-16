import random
import time
import requests
from bs4 import BeautifulSoup

MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 5  # 5 seconds, adjust as needed

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

    # Dictionary to convert month names to numbers
    "MONTH_DICTIONARY": {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }
}

def get_soup(url):
    headers = {
        'User-Agent': random.choice(CONFIG['USER_AGENTS'])
    }

    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(url, headers=headers)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error for URL {url}. Retrying...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
    # If we're here, we failed all attempts
    print(f"Failed to fetch URL {url} after {MAX_RETRIES} attempts.")
    return None


def get_soup_from_page_source(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    return soup