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
    Check if the html contains the given business name.
    :param html: html extracted from url
    :param business_name: the name of the business to look for
    :return: True if the business name is found in the html, False if not
    """
    if html is None:
        return False
    # Find all text nodes in the html
    for text in html.find_all(text=True):
        # Check if the business name appears in the text
        if business_name.lower() in text.lower():
            return True
    # The business name was not found in the html
    return False


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
