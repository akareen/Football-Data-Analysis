import random
from Config import CONFIG
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver_with_random_user_agent():
    options = Options()
    user_agent = get_random_user_agent()
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)
    return driver


def get_random_user_agent():
    return random.choice(CONFIG['USER_AGENTS'])


def set_random_user_agent(session):
    user_agent = get_random_user_agent()
    session.headers.update({'User-Agent': user_agent})