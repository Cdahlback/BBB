import bs4
import requests
import re
import csv
from time import time
import ThreadPoolExecutorPlus
from itertools import repeat


def extract_phone_data(url):
    t0 = time()
    # Either gets the response from the url, or prints the error sent
    try:
        response = requests.get(url)
        # use the response to create a soup (full html of the url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(str(e))
        print("URL {0} not found".format(url))
        # this is only so we don't finish the method call
        return -1

    # Extract phone numbers from soup using regex for phone numbers (need to modify re so it catches 5074401234)
    phone_numbers = []
    for tag in soup.find_all(text=re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')):
        phone_numbers.append(tag.string)

    print("URL: {0} data \n".format(url))
    print("PHONE NUMBERS:")
    for number in phone_numbers:
        # this if statements should not be needed
        # I added it since the regex sometimes detects the full text around the phone number, not the number itself.
        if len(number) < 15:
            print(number)

    t1 = time() - t0
    print("TIME ELAPSED: {:0.4f} sec".format(t1))
    print("------------------------")


def extract_email_data(url):
    t0 = time()
    # Either gets the response from the url, or prints the error sent
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(str(e))
        print("URL {0} not found".format(url))
        return -1

    # Extract email addresses
    email_addresses = []
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email:
            if 'mailto:' in email:
                email_addresses.append(email)

    print("URL: {0} data \n".format(url))
    print("EMAILS:")
    for email in email_addresses:
        print(email)

    t1 = time() - t0
    print("TIME ELAPSED: {:0.4f} sec".format(t1))
    print("------------------------")
    return round(t1, 5)


def get_statuscode(lst):
    """
    Gets the status code of the list of urls using threading.
    It sends a maximum of 70 (requests) threads at a time to maximize speed.

    :param lst: list of urls
    :return: a list of status codes
    """
    executor = ThreadPoolExecutorPlus.ThreadPoolExecutor(max_workers=70)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36 '
    }
    timeout = 5
    results = []
    for result in executor.map(status_code, lst, repeat(headers), repeat(timeout)):
        results.append(result)

    return results


def status_code(url, headers, timeout):
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
        return r.status_code
    except:
        return -1


inputFile = open("txt_files/urls_with_no_email.txt", "r")
inputReader = csv.reader(inputFile)

url_list = []
for row in inputReader:
    if row[0] == "1000012166":
        break
    url_list.append(row[1])

status_codes = get_statuscode(url_list)
for code in status_codes:
    print(code)

t0 = time()
times = []
for url in url_list:
    t = extract_email_data(url)
    # makes sure the time is positive ( since we return -1 if the url doesn't open )
    if t > -1:
        times.append(t)
t1 = time() - t0
print("TOTAL TIME: {0} seconds for (30) urls ran".format(t1))
print(times)
inputFile.close()
