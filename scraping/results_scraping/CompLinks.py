from ProxyScraper import ProxyScraper
from unidecode import unidecode
from Config import name_format
import json

    
def extract_league_row_info(row):
    league_name_element = row.find('th', {'data-stat': 'league_name'})
    league_name = name_format(league_name_element.text.strip())
    league_link = 'https://fbref.com' + league_name_element.find('a')['href']
    governing_body = row.find('td', {'data-stat': 'governing_body'})
    country = row.find('td', {'data-stat': 'country'})
    if governing_body:
        head_body = governing_body.text.strip()
    else:
        head_body = country.text.strip()
    return league_name, league_link, head_body


def extract_seasons_from_league_page(league_link, scraper):
    soup = scraper.get_soup_with_proxy(league_link)
    table_body = soup.find('tbody')
    if not table_body:
        return None

    year_links = table_body.find_all('th')

    year_link_dict = {}

    for year_link in year_links:
        year = year_link.text.strip()
        link = year_link.find('a')['href']
        year_link_dict[year] = 'https://fbref.com' + link
    return year_link_dict


def main():
    all_comps_url = 'https://fbref.com/en/comps/'
    scraper = ProxyScraper('scraping/results_scraping/webshare_proxies.txt')

    results = {}
    table_container_selector = 'table_container'
    soup = scraper.get_soup_with_proxy(all_comps_url)
    table_containers = soup.find_all(class_=table_container_selector)
    print(len(table_containers))

    for table in table_containers:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            league_name, league_link, head_body = extract_league_row_info(row)
            if head_body not in results:
                results[head_body] = {}
            print(f"Processing {league_name}...")
            season_results = extract_seasons_from_league_page(league_link, scraper)
            results[head_body][league_name] = season_results
            # dump results to json
            with open('output.json', 'w') as outfile:
                json.dump(results, outfile, indent=4)


if __name__ == '__main__':
    main()