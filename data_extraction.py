import bs4
import requests
import re
import csv
from time import time
import ThreadPoolExecutorPlus

from get_status_codes import get_statuscode


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


def extract_email_data(url):
    t0 = time()
    # get the html
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    # Extract email addresses
    email_addresses = []
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email:
            if 'mailto:' in email:
                email_addresses.append(email)

    # print emails for each url
    print("URL: {0} data \n".format(url))
    print("EMAILS:")
    for email in email_addresses:
        print(email)

    # display time took for specific url to extract data
    t1 = time() - t0
    print("TIME ELAPSED: {:0.4f} sec".format(t1))
    print("------------------------")
    return round(t1, 5)


# open input file
inputFile = open("txt_files/urls_with_no_email.txt", "r")
inputReader = csv.reader(inputFile)

# extract all urls from file, place them in list for our url validator
url_list = []
for row in inputReader:
    if row[0] == "1000012166":
        break
    url_list.append(row[1])

# get status code for each url
status_codes = get_statuscode(url_list)
for code in status_codes:
    print(code)

t0 = time()
times = []
for i in range(len(url_list) - 1):
    # if this url returned a -1, 400 we don't need to check it
    if status_codes[i] != 200:
        continue
    t = extract_email_data(url_list[i])
    # makes sure the time is positive ( since we return -1 if the url doesn't open )
    if t > -1:
        times.append(t)

t1 = time() - t0
print("TOTAL TIME: {0} seconds for (30) urls ran".format(t1))
print(times)

inputFile.close()
