from HelperFunctions import api_get_soup
import json

def main():
    url = 'https://www.oddsportal.com/football/results/'
    soup = api_get_soup(url)

    result = {}

    for country_div in soup.select('div.flex.items-center.w-full.h-10.gap-1.bg-gray-med_light'):
        country_name = country_div.find('span', class_='text-xs').text.strip()
        print(f"Extracting links for {country_name}...")
        links_div = country_div.find_next_sibling('div', class_='flex')

        link_urls = [f"https://www.oddsportal.com{a['href']}" for a in links_div.select('a')]
        link_text = [a.text for a in links_div.select('a')]
        
        dic = {}
        for i in range(len(link_urls)):
            current_url = link_urls[i]
            league_title = link_text[i]
            print(f"  Extracting links for {league_title}...")
            league_links = extract_league_links(current_url)

            dic[league_title] = league_links

        result[country_name] = dic


    with open("countries_links.json", "w") as outfile:
        json.dump(result, outfile, indent=4)


def extract_league_links(url: str) -> dict:
    soup = api_get_soup(url)
    # Find all divs with the class 'no-scrollbar'
    no_scrollbar_divs = soup.find_all('div', class_='no-scrollbar')

    # Select the second div from the list (if it exists)
    if len(no_scrollbar_divs) > 1:
        second_no_scrollbar_div = no_scrollbar_divs[1]
    else:
        second_no_scrollbar_div = None

    # Find all 'a' tags within the second div if it exists
    if second_no_scrollbar_div:
        links = second_no_scrollbar_div.find_all('a')
        # Extract the href attribute and text for each link
        link_dict = {link.get_text(strip=True): link.get('href') for link in links}
    else:
        link_dict = {}
    
    print(f"    Found {len(link_dict)} links.")
    return link_dict


if __name__ == "__main__":
    main()