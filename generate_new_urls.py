from create_urls import build_url_from_email, thread_search_urls
from Not_Our_Code.get_status_codes import get_statuscode_forPandas

import pandas as pd
from time import time

# read in data
data = pd.read_csv("data/text.csv", low_memory=False)

t0 = time()

# set aside all businesses that already have URLs
BBB_urls = data.loc[data['Website'].notna()]

# extract business with no URL and has email
emails_no_URL = data.loc[(data['Email'].notna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]

# extract business with no URL or email
business_no_URL_or_email = data.loc[(data['Email'].isna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]

# Extract URLs for all emails
extracted_URLs_with_emails = emails_no_URL
extracted_URLs_with_emails['Website'] = emails_no_URL['Email'].apply(lambda email: build_url_from_email(email))

# extract URLs for business without URL and email
extracted_URLs_with_search = business_no_URL_or_email.reset_index(drop=True)
print(extracted_URLs_with_search)
search_function = thread_search_urls(business_no_URL_or_email)
print(search_function)
extracted_URLs_with_search['Website'] = search_function['Website']
print(extracted_URLs_with_search)

# create Dataframe for URL with email
successful_URLs_email = extracted_URLs_with_emails.loc[extracted_URLs_with_emails['Website'].notna()]
unsuccessful_URLs_email = extracted_URLs_with_emails.loc[extracted_URLs_with_emails['Website'].isna()]

# create Dataframe for URL with search
successful_URLs_search = extracted_URLs_with_search.loc[extracted_URLs_with_search['Website'].notna()]
unsuccessful_URLs_search = extracted_URLs_with_search.loc[extracted_URLs_with_search['Website'].isna()]

# merge both Dataframes
successful_total_URLs = pd.DataFrame.append(successful_URLs_email, successful_URLs_search)

# run status code function and print to new file
status_code_DF = get_statuscode_forPandas(successful_total_URLs)

t1 = time() - t0
print(t1)

successful_status_codes = pd.merge(successful_total_URLs, status_code_DF, how='inner')
# need only URls that have acceptable status codes
successful_status_codes = successful_status_codes.loc[successful_status_codes['StatusCode'] == 200]

complied_dataframe = pd.DataFrame.append(successful_status_codes, BBB_urls)

complied_dataframe.to_csv('data/generated_urls.csv')
