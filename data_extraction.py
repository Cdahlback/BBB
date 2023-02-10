import bs4
import requests
import re
import csv
from time import time
import ThreadPoolExecutorPlus
from itertools import repeat
import pandas as pd
from get_status_codes import get_statuscode


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

    # Extract phone numbers from soup using regex for phone numbers (need to modify re so it catches 5074401234)
    phone_numbers = []
    for tag in soup.find_all(text=re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')):
        phone_numbers.append(tag.string)

    # print phone numbers from url
    print("URL: {0} data \n".format(url))
    print("PHONE NUMBERS:")
    for number in phone_numbers:
        # this if statements should not be needed
        # I added it since the regex sometimes detects the full text around the phone number, not the number itself.
        if len(number) < 15:
            print(number)

    # print time taken for specific url
    t1 = time() - t0
    print("TIME ELAPSED: {:0.4f} sec".format(t1))
    print("------------------------")


def extract_email_data(id, url):
    t0 = time()
    # get the html
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except:
        return

    # Extract email addresses
    email_addresses = {'BusinessID': id}
    email_number = 0
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email:
            if 'mailto:' in email:
                email_number += 1
                email_addresses['Email' + str(email_number)] = email
    if len(email_addresses) > 1:
        return email_addresses

    # # print emails for each url
    # print("URL: {0} data \n".format(url))
    # print("EMAILS:")
    # for email in email_addresses:
    #     print(email)
    #
    # # display time took for specific url to extract data
    # t1 = time() - t0
    # print("TIME ELAPSED: {:0.4f} sec".format(t1))
    # print("------------------------")
    # return round(t1, 5)


# open input file
# inputFile = open("txt_files/urls_with_no_email.txt", "r")
# inputReader = csv.reader(inputFile)

# pandas
data = pd.read_csv("data/mn_bbb_businesses.csv", low_memory=False)
# URLsNoEmail = data.loc[(data['Website'].notna()) & (data['Email'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Website']]
# result = [extract_email_data(id, url) for id, url in zip(URLsNoEmail['BusinessID'], URLsNoEmail['Website']) if extract_email_data(id, url) != None]
# print(result)

scraped_urls = pd.read_csv('good_emails.csv')
urls = scraped_urls['Website'].values
print(urls)

# Just for testing, more efficient ways using pandas should exist to check each url
for i, url in enumerate(urls):
    try:
        response = requests.get(url)
        html = bs4.BeautifulSoup(response.content, "html.parser")
    except:
        continue
    # print(html)
    print(url)
    print('Contains Contacts?', contains_contacts_page(html))
    print('Contains Reviews?', contains_reviews_page(html))

# urlList = URLsNoEmail['Website'].values[:100]

# extract all urls from file, place them in list for our url validator
# url_list = []
# for row in inputReader:
#     if row[0] == "1000012166":
#         break
#     url_list.append(row[1])
#
# # get status code for each url
# status_codes = get_statuscode(url_list)
# for code in status_codes:
#     print(code)
#
# t0 = time()
# times = []
# for i in range(len(url_list) - 1):
#     # if this url returned a -1, 400 we don't need to check it
#     if status_codes[i] != 200:
#         continue
#     t = extract_email_data(url_list[i])
#     # makes sure the time is positive ( since we return -1 if the url doesn't open )
#     if t > -1:
#         times.append(t)
#
# t1 = time() - t0
# print("TOTAL TIME: {0} seconds for (30) urls ran".format(t1))
# print(times)

# inputFile.close()
