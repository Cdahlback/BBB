import bs4
import requests
import re
import csv
from time import time


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


inputFile = open("txt_files/urls_with_no_email.txt", "r")
inputReader = csv.reader(inputFile)

# this is where we should split the data into 100 row blocks,
# also where we will put the multithreading when we get to that


# when we switch over to pd files instead of txt, we will have to change this for loop, since this is hardcoded ATM
t0 = time()
times = []
for row in inputReader:
    if row[0] == "1000001312":
        break
    t = extract_email_data(row[1])
    # makes sure the time is positive ( since we return -1 if the url doesn't open )
    if t > -1:
        times.append(t)
t1 = time() - t0
print("TOTAL TIME: {0} seconds for (30) urls ran".format(t1))
print(times)
inputFile.close()
