import bs4
import requests
import re
import csv
from time import time
import ThreadPoolExecutorPlus
from itertools import repeat
import pandas as pd
from get_status_codes import get_statuscode


def extract_phone_data(id, url):
    """
    Function to find phone numbers
    :param id: id associated with extracted phone #s
    :param url: url associated with extracted phone #s
    :return: dictionary of all phone #s associated with a business
    """
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(str(e))
        print("bad url")
        return None
=======
def contains_contacts_page(html):
    for tag in html.find_all('a'):
        possible_contact = tag.get('href')
        if possible_contact:
            if 'contact' in possible_contact.lower():
                return True
    return False


def contains_reviews_page(html):
    for tag in html.find_all('a'):
        possible_review = tag.get('href')
        if possible_review:
            if 'review' in possible_review.lower():
                return True
    return False


def contains_zipCode(html, zip):
    """
    :param html: url extracted html
    :param zip: business zipcode to find
    :return: True if found, false if not
    """
    for text in html.find_all(text=re.compile(r'\d{5}')):
        if re.search(str(zip), text):
            return True
    return False


def extract_phone_data(url):
    t0 = time()
    # get the html
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")
>>>>>>> IndVarFunctions

    # Extract phone numbers from soup using regex for phone numbers (need to modify re so it catches 5074401234)
    phone_numbers = {'BusinessID': id}
    counter = 0
    for tag in soup.find_all(text=re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')):
        counter += 1
        phone_numbers["Phone#{0}:".format(counter)] = tag.string

    if len(phone_numbers) >= 1:
        return phone_numbers


def extract_email_data(id, url):
    """
    Function to find emails
    :param id: id associated with extracted emails
    :param url: url associated with extracted emails
    :return: dictionary of all emails associated with a business
    """
    t0 = time()
    # get the html
    # print(id)
    # print(url)
    try:
        response = requests.get(url, timeout=5)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Excpetion as e:
        print(str(e))
        print("bad url")
        return None

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
    if len(email_addresses) > 1:
        return email_addresses


