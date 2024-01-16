from ResultsReader import ResultsReader
from HelperFunctions import sleep_randomly
from Config import get_soup

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


def extract_page_data(driver, url: str, country: str, league: str, season: str, last_scraped_date: str):
    mouse_scroll(down=True, scroll_amount=random.randint(40, 55))
    mouse_scroll(down=False, scroll_amount=random.randint(40, 55))
    
    results = []
    reader = ResultsReader()
    more_data_to_extract = True
    first_date_read = None

    while (True):
        wait_for_table(driver)
        mouse_scroll(down=True, scroll_amount=random.randint(40, 55))
        
        html = driver.page_source
        event_rows = reader.get_event_rows(html)
        print(f"Processing {len(event_rows)} rows for {country}, {league}, {season}")

        current_date = ''
        page_results = []
        for row in event_rows:
            # If the current row is a date then update the current date
            if row.select_one(reader.date_selector):
                date_text = row.select_one(reader.date_selector).text.strip()
                current_date = reader.convert_date(date_text)
            
            if last_scraped_date != '':
                if reader.is_date_before_or_equal(input_date=current_date, reference_date=last_scraped_date):
                    more_data_to_extract = False
                    results.extend(page_results)
                    print(f"Reached last scraped date: {last_scraped_date}, total processed={len(results)}")
                    return results, more_data_to_extract, first_date_read if first_date_read else last_scraped_date

            if first_date_read is None:
                first_date_read = current_date

            # If the current row is a match then read the match row data
            match_row = row.select_one(reader.match_row_selector)
            if match_row:
                data = reader.process_match_row(match_row, country, league, season, current_date)
                page_results.append(data)
        
        results.extend(page_results)

        more_pages_available = navigate_to_next_page(driver)
        if not more_pages_available:
            return results, more_data_to_extract, first_date_read if first_date_read else last_scraped_date
        
        mouse_scroll(down=False, scroll_amount=random.randint(40, 55))



def load_webpage(driver, url: str, country: str, league: str, season: str, last_scraped_date: str):
    page_num = 1
    more_pages_available = True

    results = []

    mouse_scroll(down=True, scroll_amount=random.randint(40, 55))
    mouse_scroll(down=False, scroll_amount=random.randint(40, 55))
    reader = ResultsReader()
    while (more_pages_available):
        print(f"Processing page {page_num}, of {country}, {league}, {season}")
        wait_for_table(driver)
        mouse_scroll(down=True, scroll_amount=random.randint(40, 55))
        
        
        html = driver.page_source
        to_add, last_scraped_date, reached_end = reader.read_page(html, country, league, season, last_scraped_date)

        if to_add and len(to_add) > 0:
            results.extend(to_add)

        if reached_end:
            break
        
        more_pages_available = navigate_to_next_page(driver)
        if more_pages_available is None or not more_pages_available:
            return results, last_scraped_date
        
        mouse_scroll(down=False, scroll_amount=random.randint(40, 55))
        page_num += 1

    return results, last_scraped_date


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')  # Start with maximized window
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    # Initialize the WebDriver with both Selenium Wire options and Chrome options
    driver = webdriver.Chrome(
        options=chrome_options
    )
    return driver


def wait_for_table(driver):
    css_selector = ".flex.flex-col.px-3.text-sm.max-mm\\:px-0" # Selector for the table
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    WebDriverWait(driver, 10).until(element_present)
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'eventRow'))
        WebDriverWait(driver, 5).until(element_present)
    except:
        pass


def mouse_scroll(down=True, scroll_amount=50):
    scroll_value = -scroll_amount if down else scroll_amount

    # Use PyAutoGUI to move the mouse to the middle of the screen and scroll
    screen_width, screen_height = pyautogui.size()

    pyautogui.moveTo((random.randint(5, 30) + screen_width) / 2, (random.randint(5, 30) + screen_height) / 2)

    # Scroll down in increments, with random pauses
    for _ in range(5):  # Scroll 5 increments
        pyautogui.scroll(scroll_value)  # Scroll according to the scroll value
        sleep_randomly(0.1, 0.15)  # Random pause between 0.1 to 0.15 seconds


def navigate_to_next_page(driver):
    try:
        # Click to go the next page
        sleep_randomly(0.15, 0.3)  # Random pause between 0.15 to 0.3 seconds
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
        return False

    return True


def decline_all_cookies(driver):
    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, 'onetrust-reject-all-handler'))).click()
    except TimeoutException:
        print("Cookie reject button did not appear in time.")
    except NoSuchElementException:
        print("Cookie reject button was not found on the page.")


def extract_league_links(url: str):
    soup = get_soup(url)
    no_scrollbar_divs = soup.find_all('div', class_='no-scrollbar')

    if len(no_scrollbar_divs) > 1:
        second_no_scrollbar_div = no_scrollbar_divs[1]
    else:
        second_no_scrollbar_div = None

    if second_no_scrollbar_div:
        a_links = second_no_scrollbar_div.find_all('a')
        url_links = [link.get('href') for link in a_links]
        season_names = [link.get_text(strip=True) for link in a_links]
        return url_links, season_names
    
    return [], []