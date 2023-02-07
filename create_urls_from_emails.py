import csv
import re
import pandas as pd
import validators       # Package that can validate URLs and emails with call to validate.url() or .email()

import ThreadPoolExecutorPlus
from itertools import repeat
import requests


def get_statuscode(df):
    """
    Gets the status code of the list of urls using threading.
    It sends a maximum of 70 (requests) threads at a time to maximize speed.

    :param lst: list of urls
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

# I want to take "emails_no_url.txt" as an input
# Iterate through all the emails
#   extract the domain name
#   build url around domain name
#   see what request our url gives
# add good urls to "successful_urls.txt"

# list of domain names we don't want
from elis_functions import cleanEmail

bad_domain_names = ['yahoo.com', 'gmail.com', "hotmail.com", "icloud.com", "comcast.net", "GMAIL.COM",
                    "outlook.com", "msn.com", "arvig.net", "charter.net", "winona.edu", "aol.com"]

# regex to detect valid email (works great so far, may need building upon
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


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

# create dataframe
data = pd.read_csv("data/mn_bbb_businesses.csv", low_memory=False)

emailsNoURL = data.loc[(data['Email'].notna()) & (data['Website'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Email']]
# print(emailsNoURL)
# URLsNoEmail = data.loc[(data['Website'].notna()) & (data['Email'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Website']]
# print(URLsNoEmail)
# URLsNoPhone = data.loc[(data['Website'].notna()) & (data['Phone'].isna()) & (data['BBBID'] == 704)][['BusinessID', 'Website']]
# print(URLsNoPhone)


# extract URLs for all emails
extractedURLs = emailsNoURL
extractedURLs["Website"] = emailsNoURL['Email'].apply(lambda email: build_url(email))
successfulURLs = extractedURLs.loc[extractedURLs['Website'].notna()]
# print(successfulURLs)
unsuccessfulURLs = extractedURLs.loc[extractedURLs['Website'].isna()]
# print(unsuccessfulURLs)
from time import time

t0 = time()
statusCodeDF = get_statuscode(successfulURLs)
t1 = time() - t0
print(t1)

new_df = pd.merge(successfulURLs, statusCodeDF, how='inner')

new_df = new_df.loc[new_df['StatusCode'] == 200]

new_df.to_csv('good_emails.csv')
# input file from where we get our emails
# ipt_file = open("txt_files/emails_with_no_url.txt", "r")
# ipt_reader = csv.reader(ipt_file)
#
# # Writer to the "successful_extracted_urls.txt"
# opt_file = open("txt_files/successful_extracted_urls.txt", "w")
# out_writer = csv.writer(opt_file)
#
# # Writer to the "unsuccessful_emails_to_extract_urls.txt"
# opt_file1 = open("txt_files/unsuccessful_emails_to_extract_urls.txt", "w")
# out_writer1 = csv.writer(opt_file1)

# iterate over ipt file
# for line in ipt_reader:
#     # place the business id you want to stop at (this will change once threading is introduced)
#     if line[0] == "1000003569":
#         break
#     # save email and business id
#     email = line[1]
#     business_id = line[0]
#     # get either an empty string (didn't pass build_url) or a successfully built url
#     url = build_url(email)
#     # make sure the url is not empty before writing it to the output file
#     if validators.url(url):
#         out_writer.writerow([business_id, url])
#     else:
#         out_writer1.writerow([business_id, url])

# close files
# ipt_file.close()
# opt_file.close()
# opt_file1.close()

