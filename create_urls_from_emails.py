import re
import pandas as pd
from elis_functions import cleanEmail
import ThreadPoolExecutorPlus
from itertools import repeat
import requests
from time import time
import tldextract
from googlesearch import search


# STATUS CODE FUNCTIONS
# ------------------------------------------------------------------
def get_statuscode(df):
    """
    Gets the status code of the list of urls using threading.
    It sends a maximum of 70 (requests) threads at a time to maximize speed.

    :param df: dict of urls
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


# -----------------------------------------------------------------------

# URL GENERATION METHODS
# -----------------------------------------------------------------------
def build_url(email):
    """
    :param email: email to build url from
    :return:
    If our email matches the regex and is not in our list of invalid domain names
        - Return complete URL ready to test
    If our email matches the regex, but is in our list of invalid domain names
        - Return empty string, to let the test_url function know to disregard it
    Else in case of not matching regex,
        - we return the full text of the email to investigate why we got a bad email from our extract_email function
    """
    if re.fullmatch(regex, cleanEmail(email)):
        domain_name = email.split("@")[-1]
        if domain_name not in bad_domain_names:
            return "https://www.{0}/".format(domain_name)


def getURL(company_name, Url, rating_sites):
    """
    Return company's URL given company name

    :param company_name: the name of the company
    :param Url: a list where URL is stored

    :return: company's URL if found, else return ''
    """
    try:

        term = ' '.join([company_name])
        for j in search(term, num=10, stop=10, pause=2):
            if filter(j, rating_sites):
                Url.append(j)
        return Url
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


# -----------------------------------------------------------------------

# list of domain names we don't want
bad_domain_names = ['yahoo.com', 'gmail.com', "hotmail.com", "icloud.com", "comcast.net", "GMAIL.COM",
                    "outlook.com", "msn.com", "arvig.net", "charter.net", "winona.edu", "aol.com"]

# list of rating sites for generating urls without emails.
rating_sites = ['mapquest', 'yelp', 'bbb', 'podium', 'porch', 'chamberofcommerce', 'angi']

# regex to detect valid email (works great so far, may need building upon
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

# boolean conditional to decide if to run businesses without urls and emails (for testing purpose)
run_business_with_no_url_and_email = False

# create dataframe
data = pd.read_csv("data/mn_bbb_businesses.csv", low_memory=False)

emailsNoURL = data.loc[(data['Email'].notna()) & (data['Website'].isna()) & (data['BBBID'] == 704)][
    ['BusinessID', 'Email']]

businessNoURLorEmail = data.loc[(data['Email'].isna()) & (data['Website'].isna()) & (data['BBBID'] == 704)][
    ['BusinessID', 'BusinessName']]

# extract URLs for all emails
extractedURLs_withEmail = emailsNoURL
extractedURLs_withEmail["Website"] = emailsNoURL['Email'].apply(lambda email: build_url(email))

if run_business_with_no_url_and_email:
    # extract URLs for business without URL and email
    extractedURLs_noEmail = businessNoURLorEmail
    extractedURLs_noEmail['Website'] = businessNoURLorEmail['BusinessName'].apply(
        lambda company_name: getURL(company_name, [], rating_sites))

if run_business_with_no_url_and_email:
    # combine all successful URLs and businesses with still no URL
    successfulURLs = (extractedURLs_withEmail.loc[extractedURLs_withEmail['Website'].notna()]) & (extractedURLs_noEmail.loc[
        extractedURLs_noEmail['Website'].notna()])
    unsuccessfulURLs = (extractedURLs_withEmail.loc[extractedURLs_withEmail['Website'].isna()]) & (
        extractedURLs_noEmail.loc[extractedURLs_noEmail['Website'].isna()])
else:
    successfulURLs = extractedURLs_withEmail.loc[extractedURLs_withEmail['Website'].notna()]
    unsuccessfulURLs = extractedURLs_withEmail.loc[extractedURLs_withEmail['Website'].isna()]

t0 = time()
statusCodeDF = get_statuscode(successfulURLs)
t1 = time() - t0
print(t1)

new_df = pd.merge(successfulURLs, statusCodeDF, how='inner')

new_df = new_df.loc[new_df['StatusCode'] == 200]

new_df.to_csv('good_emails.csv')
