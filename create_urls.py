import re
from Not_Our_Code.elis_functions import cleanEmail
from googlesearch import search
import tldextract
import ThreadPoolExecutorPlus
import pandas as pd
from itertools import repeat
from time import sleep
from tldextract import tldextract

"""
For CODE REVIEWER:
We have two functions which build new urls for us

- build_url_from_email:
    - This function relies on the specific row in our csv file HAVING an EMAIL, but MISSING a URL
    - Returns the new url formed from the email, if it passes our checks

(from previous bbb team)
- get_url_from_search: 
    - makes use of a helper function (filter), which removes a site in our list if it is in our rating_sites
    - This function uses the given Company Name to search on the web for that companies website
    - 10 potential urls are extracted (excluding rating_sites) and the best match is returned
        - We may modify it if we find these urls are "bad" (aren't related to the company)
    - return the top url of choice from our algo
    

"""

# list of domain names we don't want
bad_domain_names = ['yahoo.com', 'gmail.com', "hotmail.com", "icloud.com", "comcast.net", "GMAIL.COM",
                    "outlook.com", "msn.com", "arvig.net", "charter.net", "winona.edu", "aol.com", "frontier.net",
                    "frontiernet.net", "results.net"]

# regex to detect valid email (works great so far, may need building upon
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# list of rating sites for generating urls without emails.
rating_sites = ['mapquest', 'yelp', 'bbb', 'podium', 'porch', 'chamberofcommerce', 'angi']


def build_url_from_email(email):
    """
    :param email: email to build url from
    :return: Formatted url extracted from email
    """
    if re.fullmatch(email_regex, cleanEmail(email)):
        domain_name = email.split("@")[-1]
        if domain_name not in bad_domain_names:
            return "https://www.{0}/".format(domain_name)


def thread_search_urls(df):
    """
    Gets the status code of the list of urls using threading.
    It sends a maximum of 70 (requests) threads at a time to maximize speed.

    :param df: list of urls
    :return: a list of status codes
    """
    executor = ThreadPoolExecutorPlus.ThreadPoolExecutor(max_workers=50)
    results = []
    rating_sites = ['mapquest', 'yelp', 'bbb', 'podium', 'porch', 'chamberofcommerce', 'angi']
    business_names = df['BusinessName'].tolist()
    business_cities = df['City'].tolist()
    business_id = df['BusinessID'].tolist()
    for result in executor.map(get_url_from_search, business_names, repeat(rating_sites), business_id, business_cities):
        results.append(result)
    return pd.DataFrame(results, columns=['BusinessID', 'Website'])


def get_url_from_search(company_name, rating_sites, business_id, company_city_state=""):
    """
    Return company's URL given company name

    :param company_name: the name of the company
    :return: company's URL if found, else return ''
    """
    if pd.isnull(company_city_state):
        company_city_state = ""
    term = ' '.join([company_name, company_city_state])
    businessid_and_website = {}
    for j in search(term, num_results=10):
        if filter(j, rating_sites):
            print(business_id, j)
            return business_id, j
        else:
            continue

    print(business_id, '')
    return business_id, ''



def filter(url, rating_sites):
    """
    A function that checks if found url are rating sites
    Helper method to get_url_from_search

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
