from ProxyScraper import ProxyScraper
import csv


class PlayerScraper:
    all_players_links = []


    def __init__(self, url):
        self.url = url
        self.scraper = ProxyScraper('scraping/results_scraping/webshare_proxies.txt')
        self.players_url = 'https://fbref.com/en/players/'
        self.output_csv_file_path = 'scraping/results_scraping/data/player_links.csv'
        self.all_players_links = self.get_all_player_links()
        self.write_to_csv(self.all_players_links)


    def get_all_player_links(self):
        by_two_letter_code = self.get_links_from_section_wrapper(self.players_url, self.scraper)[1:-3]
        all_players_links = []

        for letter_link in by_two_letter_code:
            print(f"Retrieving players from {letter_link}...")
            letter_results = self.get_links_from_section_wrapper(letter_link, self.scraper)[:-4]
            all_players_links.extend(letter_results)

        print(f"Number of players retrieved: {len(all_players_links)}")

        return all_players_links


    def get_links_from_section_wrapper(self, url, scraper):
        base_url = "https://fbref.com"
        soup = scraper.get_soup_with_proxy(url)

        section_wrappers = soup.find_all(class_='section_wrapper')

        links = []
        for wrapper in section_wrappers:
            for a in wrapper.find_all('a', href=True):
                link = a['href']
                if link.startswith('/'):
                    full_url = base_url + link
                    links.append(full_url)

        return links


    def write_to_csv(self, data):
        with open(self.output_csv_file_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)