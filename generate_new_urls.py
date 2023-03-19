from create_urls import build_url_from_email, thread_search_urls
from get_status_codes import get_statuscode_forPandas

import pandas as pd
from time import time

# read in data
data = pd.read_csv("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSPROJECT1/BBB/data/mn_bbb_businesses.csv", low_memory=False)

"""Add urls from search"""

# set aside all businesses that already have URLs
BBB_urls = data.loc[data['Website'].notna()]

# extract business with no URL and has email
emails_no_URL = data.loc[(data['Email'].notna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]

# extract business with no URL or email
business_no_URL_and_email = data.loc[(data['Email'].isna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]
business_no_URL_and_email = business_no_URL_and_email.head(5000)

# runtime for url generation
generation_time = time()

# Extract URLs for all emails
extracted_URLs_with_emails = emails_no_URL
extracted_URLs_with_emails['Website'] = emails_no_URL['Email'].apply(lambda email: build_url_from_email(email))

# extract URLs for business without URL and email
search_function = thread_search_urls(business_no_URL_and_email)
missing_websites = search_function['Website'].tolist()
business_no_URL_and_email['Website'] = missing_websites
extracted_URLs_with_search = business_no_URL_and_email.reset_index(drop=True)

t1 = time() - generation_time
print("URL Generation runtime: ".format(t1))

"""Add urls from email"""

# create Dataframe for URL with email
successful_URLs_email = extracted_URLs_with_emails.loc[extracted_URLs_with_emails['Website'].notna()]
unsuccessful_URLs_email = extracted_URLs_with_emails.loc[extracted_URLs_with_emails['Website'].isna()]

# create Dataframe for URL with search
successful_URLs_search = extracted_URLs_with_search.loc[extracted_URLs_with_search['Website'].notna()]
unsuccessful_URLs_search = extracted_URLs_with_search.loc[extracted_URLs_with_search['Website'].isna()]

# merge both Dataframes
successful_total_URLs = pd.DataFrame.append(successful_URLs_email, successful_URLs_search)

# runtime for status code function
status_time = time()

# run status code function and print to new file
status_code_DF = get_statuscode_forPandas(successful_total_URLs)

t2 = time() - status_time
print("Status code runtime: {0}".format(t2))

successful_status_codes = pd.merge(successful_total_URLs, status_code_DF, how='inner')
# need only URls that have acceptable status codes
successful_status_codes = successful_status_codes.loc[(successful_status_codes['StatusCode'] >= 200) &
                                                      (successful_status_codes['StatusCode'] < 400)]

complied_dataframe = pd.DataFrame.append(BBB_urls, successful_status_codes)
complied_dataframe.reset_index(drop=True)

complied_dataframe.to_csv('data/generated_urls.csv', index=False)
