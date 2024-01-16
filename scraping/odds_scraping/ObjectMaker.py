from HelperFunctions import get_soup
from unidecode import unidecode
import json

def make_new_object(json_location):
    url = 'https://www.oddsportal.com/football/results/'
    soup = get_soup(url)

    result = {}

    for country_div in soup.select('div.flex.items-center.w-full.h-10.gap-1.bg-gray-med_light'):
        country_name = name_format(country_div.find('span', class_='text-xs').text.strip())
        links_div = country_div.find_next_sibling('div', class_='flex')

        link_urls = [f"https://www.oddsportal.com{a['href']}" for a in links_div.select('a')]
        link_text = [a.text for a in links_div.select('a')]
        
        dic = {}
        for i in range(len(link_urls)):
            league_name = name_format(link_text[i])
            dic[league_name] = {}
            url = link_urls[i]
            dic[league_name]['url'] = url
            dic[league_name]['last_scraped_date'] = ''
             
        result[country_name] = dic


    with open(json_location, "w") as outfile:
        json.dump(result, outfile, indent=4)


def update_object(input_location, output_location):
    url = 'https://www.oddsportal.com/football/results/'
    soup = get_soup(url)

    with open(input_location) as json_file:
        data = json.load(json_file)
    
    for country_div in soup.select('div.flex.items-center.w-full.h-10.gap-1.bg-gray-med_light'):
        country_name = name_format(country_div.find('span', class_='text-xs').text.strip())
        links_div = country_div.find_next_sibling('div', class_='flex')

        link_urls = [f"https://www.oddsportal.com{a['href']}" for a in links_div.select('a')]
        link_text = [a.text for a in links_div.select('a')]
        
        if country_name not in data:
            data[country_name] = {}
        for i in range(len(link_urls)):
            league_name = name_format(link_text[i])
            if league_name not in data[country_name]:
                league_dic = {}
                league_dic['url'] = link_urls[i]
                league_dic['last_scraped_date'] = ''
                data[country_name][league_name] = league_dic

    with open(output_location, "w") as outfile:
        json.dump(data, outfile, indent=4)


def name_format(name):
    name = unidecode(name)
    formatted_name = name.strip().replace(" ", '-')
    formatted_name = formatted_name.replace('/', '-')
    while '--' in formatted_name:
        formatted_name = formatted_name.replace('--', '-')
    return formatted_name.upper()