import bs4
from bs4 import BeautifulSoup
import requests
import re
import whois
from urllib.parse import urlparse
import numpy as np
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
    '''
    Checks for a contacts page inside a webpage
    :param html: html extracted from url
    :return: True if found, False if not
    '''
    if html is not None:
        for tag in html.find_all('a'):
            possible_contact = tag.get('href')
            if possible_contact:
                if 'contact' in possible_contact.lower():
                    return True
        return False
    else:
        return np.nan


def contains_business_name(html, business_name):
    """
    Check if the soup contains the given business name.
    :param html: html extracted from url
    :param business_name: the name of the business to look for
    :return: True if found, False if not
    """
    if html is not None:
        # Find all text nodes in the soup
        for text in html.find_all(text=True):
            # Check if the business name appears in the text
            if business_name.lower() in text.lower():
                return True
        # The business name was not found in the soup
        return False
    else:
        return np.nan


# def contains_business_name_in_copyright(html, BusinessName):
#     """
#     Check if the soup contains the given business name.
#     :param html: html extracted from url
#     :param business_name: the name of the business to look for
#     :return: True if found, False if not
#     """
#     if html is not None:
#         for text in html.find_all(text=u"\N{COPYRIGHT SIGN}"):
#             if BusinessName.lower() in text.lower():
#                 return True
#         return False
#     else:
#         return np.nan

def contains_business_name_in_copyright(html, business_name):
    """
    Check if the given business name is present in the footer of the website by comparing the number of matching words
    in the footer text and the business name. If at least 50% of the words in the business name are found in the footer text,
    the function returns True. Otherwise, it returns False.
    param html (BeautifulSoup object): The parsed HTML content of the website.
    param business_name (str): The name of the business to search for.
    Returns: True if the business name is found in the footer of the website, False otherwise.
    """

    if html is not None:
        try:
            footer = html.find('footer')
            if footer is not None:
                footer_text = footer.text
                footer_text_words = re.findall(r'\b\w+\b', footer_text.lower())  # extract all words from the footer text
                business_name_words = re.findall(r'\b\w+\b', business_name.lower())
                matches = set(footer_text_words) & set(business_name_words) # get the set of words that appear in both footer and business name
                num_matches = len(matches)
                if num_matches >= len(business_name_words) / 2:
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            return False


def contains_social_media_links(html):
    """
    Question: Should we look for how many social media pages it has?
    Check if the soup contains a social media section.
    :param html:
    :return:
    """
    if html is not None:
        links = html.find_all('a')
        # Check each link to see if it points to a social media website
        social_media_sites = ['facebook', 'twitter', 'instagram', 'linkedin']
        for link in links:
            href = link.get('href')
            if href and any(site in href.lower() for site in social_media_sites):
                return True
        # If we didn't find any social media links, return False
        return False
    else:
        return np.nan


def contains_reviews_page(html):
    '''
    Checks for a reviews page inside the webpage
    :param html: html extracted from url
    :return: True if found, False if not
    '''
    if html is not None:
        for tag in html.find_all('a'):
            possible_review = tag.get('href')
            if possible_review:
                if 'review' in possible_review.lower():
                    return True
        return False
    else:
        return np.nan


def contains_zipCode(html, zip):
    """
    :param html: url extracted html
    :param zip: business zipcode to find
    :return: True if found, false if not
    """
    if pd.isnull(zip):
        return False
    if html is not None:
        for text in html.find_all(text=re.compile(r'\d{5}')):
            if re.search(str(zip), text):
                return True
        return False
    else:
        return np.nan


def url_contains_phone_number(html, number):
    """
    Checks if the phone number for this business is in teh html
    :param html:
    :param number:
    :return:
    """
    if pd.isnull(number):
        return False
    if html is not None:
        for text in html.find_all(text=True):
            if str(number) in text.replace("-", ""):
                return True
        return False
    else:
        return np.nan


def url_contains_email(html, email):
    if html is not None and email is not None:
        if pd.isnull(email):
            return False
        for tag in html.find_all('a'):
            href = tag.get('href')
            if href is None:
                return False
            if email in href:
                return True
        return False
    else:
        return np.nan


def get_domain_owner(url):
    domain = urlparse(url).netloc
    try:
        w = whois.whois(domain)
    except Exception:
        return ""
    else:
        return w.registrar


def extract_phone_data(BusinessID, Website):
    """
    Function to find phone numbers
    :param id: id associated with extracted phone #s
    :param url: url associated with extracted phone #s
    :return: dictionary of all phone #s associated with a business
    """
    try:
        response = requests.get(Website)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(str(e))
        print("bad url")
        return None

    # Extract phone numbers from soup using regex for phone numbers (need to modify re so it catches 5074401234)
    phone_numbers = {'BusinessID': BusinessID}
    counter = 0
    for tag in soup.find_all(text=re.compile(r'(?\d{3})?[-.\s]?\d{3}[-.\s]?\d{4}')):
        counter += 1
        phone_numbers["Phone#{0}:".format(counter)] = tag.string

    if len(phone_numbers) >= 1:
        return phone_numbers

def extract_email_data(BusinessID, Website):
    """
    Function to find emails
    :param id: id associated with extracted emails
    :param url: url associated with extracted emails
    :return: dictionary of all emails associated with a business
    """
    try:
        response = requests.get(Website)
        soup = BeautifulSoup(response.content, "html.parser")
    except:
        return

    # Extract email addresses
    email_addresses = {'BusinessID': id}
    email_number = 0
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email:
            if 'mailto:' in email:
                if email in email_addresses:
                    continue
                email_number += 1
                email_addresses['Email' + str(email_number)] = email
    if len(email_addresses) >= 1:
        return email_addresses