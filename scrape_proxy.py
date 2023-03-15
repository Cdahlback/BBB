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

url = 'https://free-proxy-list.net/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('ID Adrress')

https_proxies = []

for row in table.find_all('<tr>'):
    cells = row.find_all('<td>')
    if len(cells) > 6 and cells[6].get_text() == 'yes':
        https_proxies.append(cells[0].get_text())

print(https_proxies)
