# import requests
# import re
#
# url = 'https://free-proxy-list.net/'
#
# response = requests.get(url)
#
# ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
#
# ip_addresses = re.findall(ip_pattern, response.text)
#
# print(ip_addresses)
#

import requests
from bs4 import BeautifulSoup

def scrape_https_proxies(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    data = []
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if cols and cols[6].get_text() == 'yes':
            data.append(cols[0].get_text())
    return data

url = 'https://free-proxy-list.net/'
https_proxies = scrape_https_proxies(url)
print(https_proxies)
