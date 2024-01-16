import requests
from bs4 import BeautifulSoup
from itertools import cycle

class ProxyScraper:
    def __init__(self, proxy_file_path):
        self.proxies = self.load_proxies_from_file(proxy_file_path)
        self.proxy_pool = cycle(self.proxies)

    def load_proxies_from_file(self, file_path):
        with open(file_path, 'r') as file:
            proxies = file.read().splitlines()
        return proxies

    
    def get_soup_with_proxy(self, url):
        result = self.get_method(url)
        while result is None:
            result = self.get_method(url)
        return result


    def get_method(self, url):
        try:
            # Get the next proxy from the cycle
            selected_proxy = next(self.proxy_pool)
            print(f"Using proxy {selected_proxy}")

            # Split the proxy string into parts
            proxy_parts = selected_proxy.split(":")
            if len(proxy_parts) == 4:
                ip, port, username, password = proxy_parts
                proxy_string = f"{username}:{password}@{ip}:{port}"
            elif len(proxy_parts) == 2:
                ip, port = proxy_parts
                proxy_string = f"{ip}:{port}"
            else:
                raise ValueError("Invalid proxy format")

            # Determine if the proxy should use HTTP or HTTPS
            if url.startswith("https://"):
                proxy_url = f"http://{proxy_string}"
            else:
                proxy_url = f"https://{proxy_string}"

            # Define proxy settings for the current request
            proxy_dict = {
                "http": proxy_url,
                "https": proxy_url
            }
            # Send a GET request with the selected proxy
            response = requests.get(url, proxies=proxy_dict, timeout=5)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup

        except Exception as e:
            print(f"Proxy {selected_proxy} failed: {str(e)}")

        # If the selected proxy fails, return None
        return None