from ResultsReader import ResultsReader
from HelperFunctions import sleep_randomly

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pyautogui
import time
import random
from pyvirtualdisplay import Display


def load_webpage(driver, url: str, country: str, league: str, season: str):
    page_num = 1
    more_pages_available = True

    results = []

    mouse_scroll(down=True, scroll_amount=random.randint(45, 60))
    mouse_scroll(down=False, scroll_amount=random.randint(45, 60))
    reader = ResultsReader()
    while (more_pages_available):
        print(f"Processing page {page_num}, of {country}, {league}, {season}")
        wait_for_table(driver)
        mouse_scroll(down=True, scroll_amount=random.randint(45, 60))
        
        
        html = driver.page_source
        results.extend(reader.read_page(html, country, league, season))

        more_pages_available = navigate_to_next_page(driver)
        if more_pages_available is None:
            return None
        
        mouse_scroll(down=False, scroll_amount=random.randint(45, 60))
        page_num += 1

    return results


def create_driver_server(chrome_driver_path='/path/to/chromedriver', 
                         user_agent=None, 
                         window_size=(800, 600),
                         display_visible=0):
    # Start the virtual display
    display = Display(visible=display_visible, size=window_size)
    display.start()

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    if user_agent:
        options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    options.add_argument('--headless')
    
    # Create the Chrome WebDriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    return driver, display


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')  # Start with maximized window

    # Initialize the WebDriver with both Selenium Wire options and Chrome options
    driver = webdriver.Chrome(
        options=chrome_options
    )
    return driver


def wait_for_table(driver):
    css_selector = ".flex.flex-col.px-3.text-sm.max-mm\\:px-0" # Selector for the table
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    WebDriverWait(driver, 10).until(element_present)


def mouse_scroll(down=True, scroll_amount=50):
    scroll_value = -scroll_amount if down else scroll_amount

    # Use PyAutoGUI to move the mouse to the middle of the screen and scroll
    screen_width, screen_height = pyautogui.size()

    pyautogui.moveTo((random.randint(5, 30) + screen_width) / 2, (random.randint(5, 30) + screen_height) / 2)

    # Scroll down in increments, with random pauses
    for _ in range(10):  # Scroll 10 increments
        pyautogui.scroll(scroll_value)  # Scroll according to the scroll value
        sleep_randomly(0.1, 0.2)  # Random pause between 0.1 to 0.2 seconds


def navigate_to_next_page(driver):
    try:
        # Click to go the next page
        time.sleep(random.uniform(0.5, 1))
        next_page_div_selector = ".pagination.my-7.flex.items-center.justify-center"
        next_page_div = driver.find_element(By.CSS_SELECTOR, next_page_div_selector)
        last_elem_next_page_div = None

        # If the last element's text is "Next" click it
        last_elem_next_page_div = next_page_div.find_elements(By.TAG_NAME, 'a')[-1]     

        if last_elem_next_page_div.text.strip() == "Next":
            driver.execute_script("arguments[0].click();", last_elem_next_page_div)
            wait_for_table(driver)
        else:
            # If not break out of the loop as it has reached the end of processing
            return False
    except NoSuchElementException:
        print(f"No next page found")
        return False
    except Exception as e:
        print(f"Error with the next page div: {e}")
        return None

    return True

def decline_all_cookies(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))).click()
    except TimeoutException:
        print("Cookie reject button did not appear in time.")
    except NoSuchElementException:
        print("Cookie reject button was not found on the page.")