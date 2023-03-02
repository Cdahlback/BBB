from tldextract import tldextract
from googlesearch import search

"""From generate_urls.py from previous teams repo"""


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