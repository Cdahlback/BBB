from create_urls import build_url_from_email, get_url_from_search, rating_sites
from Not_Our_Code.get_status_codes import get_statuscode_forPandas

import pandas as pd
from time import time

# read in data
data = pd.read_csv("data/text.csv", low_memory=False)

t0 = time()

# extract business with no URL and has email
emails_no_URL = data.loc[(data['Email'].notna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]

# extract business with no URL or email
business_no_URL_or_email = data.loc[(data['Email'].isna()) & (data['Website'].isna()) & (data['BBBID'] == 704)]

# Extract URLs for all emails
extracted_URLs_with_emails = emails_no_URL
extracted_URLs_with_emails['Website'] = emails_no_URL['Email'].apply(lambda email: build_url_from_email(email))

# extract URLs for business without URL and email
extracted_URLs_with_search = business_no_URL_or_email
extracted_URLs_with_search['Website'] = business_no_URL_or_email['BusinessName'].apply(lambda company_name:
                                                            get_url_from_search(company_name, rating_sites))

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

compiled_dataframe = pd.merge(successful_total_URLs, status_code_DF, how='inner')
# need only URls that have acceptable status codes
compiled_dataframe = compiled_dataframe.loc[compiled_dataframe['StatusCode'] == 200]

compiled_dataframe.to_csv('data/generated_urls.csv')
