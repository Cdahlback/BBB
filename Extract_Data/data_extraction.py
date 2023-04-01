import bs4
from bs4 import BeautifulSoup
import requests
import re
import whois
from urllib.parse import urlparse
import pandas as pd


"""
For CODE REVIEWER:
This file is used to hold all our functions which extract data from a url
There are two types of functions you see here, listed below
- functions which start with "contains"
    - These functions scrape html/soup for independent variables we plan to use in our ML model 
      (don't know what model will work best quite yet)
    - Return a 0 or 1 which tells us if the ind var was found within our html/soup
- functions which start with extract
    - Scrape html/soup for data types we are looking to fill in our csv file (emails, phone#s, addresses)
    - Return the data type(s) we found from that single html/soup
"""


def contains_contacts_page(html):
    """
    Check if the html contains a contacts page.
    :param html: html extracted from url
    :return: True if a contacts page is found in the html, False if not
    """
    if html is None:
        return False
    # Find all a tags in the html
    for tag in html.find_all('a'):
        # Get the next href link and check if it contains the word contact
        possible_contact = tag.get('href')
        if possible_contact and 'contact' in possible_contact.lower():
            return True
    # No contacts page was found
    return False


def contains_business_name(html, business_name):
    """
    check if the business name is in the url/html
    :param html: html input from website
    :param business_name: name of business we want to find
    :return: bool True of False
    """
    if business_name == '':
        return False
    if html is not None:
        # remove '&#39;' from string and replace with '
        if re.search(r'&#39;', business_name):
            business_name = re.sub('&#39;', '\'', business_name)
        # remove any floating non-letter characters
        if re.search(r'\s\W\s', business_name):
            business_name = re.sub(r'\s\W\s', ' ', business_name)
        # remove any non-letter/digit characters
        business_name = re.sub(r'[^A-Za-z0-9\'\s]*', '', business_name)
        name_lst = business_name.split()        # split business_name into list of words
        found_name = 0                  # counter for every word in the list found on the html
        for name in name_lst:           # loop through word in list
            found = False
            for text in html.find_all(text=True):
                if name.lower() in text.lower():
                    found = True        # found is mark true if word was found in html
            if found:
                found_name += 1         # add to counter
        if found_name / len(name_lst) >= 0.5:     # if more than half of the words in the list were found in the html
            return True                          # then return True
        else:
            return False
    else:
        return None


def contains_business_name_in_copyright(html, business_name):
    """
    Check if the given business name is present in the footer of the website by comparing the number of matching words
    in the footer text and the business name. If at least 50% of the words in the business name are found in the footer
    text, the function returns True. Otherwise, it returns False.
    :param html: (BeautifulSoup object): The parsed HTML content of the website
    :param business_name: (str): The name of the business to search for
    :return: True if the business name is found in the footer of the website, False otherwise
    """
    if html is None:
        return False
    try:
        footer = html.find('footer')
        if footer is None:
            return False
        footer_text = footer.text
        # Extract all words from the footer text
        footer_text_words = re.findall(r'\b\w+\b', footer_text.lower())
        business_name_words = re.findall(r'\b\w+\b', business_name.lower())
        # Get the set of words that appear in both footer and business name
        matches = set(footer_text_words) & set(business_name_words)
        num_matches = len(matches)
        return num_matches >= len(business_name_words) / 2
    except Exception:
        return False


def contains_social_media_links(html):
    """
    Check if the html contains a social media section.
    :param html: html extracted from url
    :return: True if a social media section is found in the html, False if not
    """
    if html is None:
        return False
    links = html.find_all('a')
    # Check each link to see if it points to a social media website
    social_media_sites = ['facebook', 'twitter', 'instagram', 'linkedin']
    for link in links:
        href = link.get('href')
        if href and any(site in href.lower() for site in social_media_sites):
            return True
    # If we didn't find any social media links, return False
    return False


def contains_reviews_page(html):
    """
    Check if the html contains a reviews page.
    :param html: html extracted from url
    :return: True if a reviews page is found in the html, False if not
    """
    if html is None:
        return False
    for tag in html.find_all('a'):
        possible_review = tag.get('href')
        if possible_review and 'review' in possible_review.lower():
            return True
    return False


def contains_zipCode(html, zip_code):
    """
    Check if the html contains the given zip code.
    :param html: html extracted from url
    :param zip_code: business zip code to find
    :return: True if the zip code is found in the html, False if not
    """
    if pd.isnull(zip_code) or html is None:
        return False
    for text in html.find_all(text=re.compile(r'\d{5}')):
        if re.search(str(zip_code), text):
            return True


def contains_phone_number(html, phone_number):
    """
    Check if the html contains the given phone number
    :param html: html extracted from url
    :param phone_number: business phone number to find
    :return: True if the phone number is found in the html, False if not
    """
    if pd.isnull(phone_number) or html is None:
        return False
    for text in html.find_all(text=True):
        if str(phone_number) in text.replace("-", ""):
            return True
    return False


def contains_email(html, email):
    """
    Check if the html contains the given email address
    :param html: html extracted from url
    :param email: business email address to find
    :return: True if the email address is found in the html, False if not
    """
    if pd.isnull(email) or html is None:
        return False
    for tag in html.find_all('a'):
        href = tag.get('href')
        if email in href:
            return True
    return False


def get_domain_owner(url):
    """
    Gets the name of the owner for the given url's domain
    :param url: url to check the domain owner of
    :return: A string containing the name of the domain owner, an empty string if the name can't be found
    """
    domain = urlparse(url).netloc
    try:
        w = whois.whois(domain)
    except Exception:
        return ""
    else:
        return w.registrar


def url_is_review_page(url, html):
    """
    checks if url is a review page by looking at url strong contents
    :param url: input url
    :param html: the html of the url parameter
    :return: True if url is a review page, false if not
    """
    # list of rating sites we have already excluded from search.
    rating_sites = ['mapquest', 'yelp', 'bbb', 'podium', 'porch', 'chamberofcommerce', 'angi', 'yellowpages',
                    'bizapedia']
    # list of phrases that would indicate if the url is a review page.
    indicator_list = ['/businessdirectory/', '/pages/', '/restaurants/', '/companies/', '/businesses/',
                      '/contractor/', '/profile/', '/company-information/', '/directory/']
    # Case 1: looping through the rating sites we already excluded from our search, making sure none slipped through.
    for site in rating_sites:
        if site in url.lower():
            return True
    # Case 2: if the url contains an indicator in the list, it will return true.
    for indicator in indicator_list:
        if indicator in url.lower():
            return True
    # Case 3: if the word 'review' appears in the html text, return true.
    for text in html.find_all(text=True):
        if 'review' in text.lower():
            return True
    # if no cases apply, return false
    return False


def extract_phone_data(business_id, url):
    """
    Finds phone numbers in the given url's webpage
    :param business_id: id associated with a business
    :param url: url to search for phone numbers in
    :return: dictionary of all phone numbers found in the given url's webpage
    """
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Exception:
        return None

    # Extract phone numbers from soup using regex for phone numbers
    phone_numbers = {'BusinessID': business_id}
    counter = 0
    for tag in soup.find_all(text=re.compile(r'(?\d{3})?[-.\s]?\d{3}[-.\s]?\d{4}')):
        counter += 1
        phone_numbers["Phone#{0}:".format(counter)] = tag.string

    if len(phone_numbers) >= 1:
        return phone_numbers


def extract_email_data(business_id, url):
    """
    Finds email addresses in the given url's webpage
    :param business_id: id associated with a business
    :param url: url to search for emails in
    :return: dictionary of all emails found in the given url's webpage
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception:
        return None

    # Extract email addresses
    email_addresses = {'BusinessID': business_id}
    email_number = 0
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email and 'mailto:' in email:
            if email in email_addresses:
                continue
            email_number += 1
            email_addresses['Email' + str(email_number)] = email
    if len(email_addresses) >= 1:
        return email_addresses
