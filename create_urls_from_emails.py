import csv
import re
import requests
import ThreadPoolExecutorPlus
import pandas as pd

from elis_functions import cleanEmail
from itertools import repeat

# list of domain names we don't want
bad_domain_names = ['yahoo.com', 'gmail.com', "hotmail.com", "icloud.com", "comcast.net", "GMAIL.COM",
                    "outlook.com", "msn.com", "arvig.net", "charter.net", "winona.edu", "aol.com"]

# regex to detect valid email (works great so far, may need building upon
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def get_statuscode(df):
    """
    Gets the status code of the list of urls using threading.
    It sends a maximum of 70 (requests) threads at a time to maximize speed.

    :param lst: list of urls
    :return: a list of status codes
    """
    urls = df['Website'].values[:50]
    ids = df['BusinessID'].values[:50]
    executor = ThreadPoolExecutorPlus.ThreadPoolExecutor(max_workers=70)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36 '
    }
    timeout = 5
    results = []
    for result in executor.map(status_code, urls, ids, repeat(headers), repeat(timeout)):
        results.append(result)
    return pd.DataFrame(results, columns=['BusinessID', 'StatusCode'])


def status_code(url, id, headers, timeout):
    """
    Gets a single url and returns the status code

    :param url: a single url
    :param headers: a dictionary that contains user agent strings.
    User agent string is contained in the HTTP headers and is intended to identify devices requesting online content.
    :param timeout: limits the maximum time for calling a function
    :return: status code of the url if it receives a response within the given time, if not returns -1
    """
    try:
        r = requests.get(url, verify=True, timeout=timeout, headers=headers)
        return id, r.status_code
    except:
        return id, -1


def build_url(email):
    """
    :param email: email to build url from
    :return: Formatted url extracted from email
    """
    if re.fullmatch(email_regex, cleanEmail(email)):
        domain_name = email.split("@")[-1]
        if domain_name not in bad_domain_names:
            return "https://www.{0}/".format(domain_name)


def getURL(company_name, rating_sites):
    """
    Return company's URL given company name

    :param company_name: the name of the company
    :return: company's URL if found, else return ''
    """
    try:

        term = ' '.join([company_name])
        for j in search(term, num=10, stop=10, pause=2):
            if filter(j, rating_sites):
                return j
            else:
                continue
    except:
        return ''


def filter(url, rating_sites):
    """
    A function that checks if found url are rating sites

    :param url: the url
    :param rating_sites: list of any known rating sites
    :return: True if url is a not a rating site, false otherwise
    """
    sub = tldextract.extract(url)
    # print("Subdomain ", sub.domain)
    for i in rating_sites:
        if sub.domain.lower() == i:
            return False
    return True


# emailsNoURL = data.loc[(data['Email'].notna()) & (data['Website'].isna())][['BusinessID', 'Email']]
# URLsNoEmail = data.loc[(data['Website'].notna()) & (data['Email'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Website']]
# URLsNoPhone = data.loc[(data['Website'].notna()) & (data['Phone'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Website']]

