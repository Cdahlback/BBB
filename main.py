from create_urls import build_url_from_email
from Not_Our_Code.get_status_codes import get_statuscode, status_code
from data_extraction import extract_email_data, extract_phone_data
from time import time

import pandas as pd


def extract_urls_from_emails(data):
    """
    Function to create urls from email domains.
    :param data: passed in dataframe from main
    :return: New DataFrame with columns BusinessID, Website.
    """
    emails_no_url = data.loc[(data['Email'].notna()) & (data['Website'].isna())][['BusinessID', 'Email']]

    # extract URLs for all emails without urls
    extracted_urls = emails_no_url
    extracted_urls["Website"] = emails_no_url['Email'].apply(lambda email: build_url_from_email(email))
    successful_urls = extracted_urls.loc[extracted_urls['Website'].notna()]

    # prints the time taken (For testing purposes, can be removed for PROD)
    t0 = time()
    status_code_df = get_statuscode(successful_urls)
    t1 = time() - t0
    print(t1)

    # merge successful_urls with status codes given
    new_df = pd.merge(successful_urls, status_code_df, how='inner')
    new_df = new_df.loc[(new_df['StatusCode'] != 404) & (new_df['StatusCode'] != -1) & (new_df['StatusCode'] != 403)]
    return new_df


def extract_emails_from_urls(data):
    """
    Extract ALL emails from ALL websites
    :param data: dataframe from where we get our urls
    :return: list of dictionaries containing the businessID and all emails found
    """
    websites_no_emails = data.loc[(data['Email'].isna()) & (data['Website'].notna())][["BusinessID", "Website"]]
    result = [extract_email_data(id, url) for id, url in
              zip(websites_no_emails['BusinessID'], websites_no_emails['Website']) if
              extract_email_data(id, url) is not None]
    return result


def merge_new_data(df1, df2):
    """

    :param df1: dataset which to append values to
    :param df2: dataset used to fill in values
    :return: dataset with filled in values
    """
    df1.reset_index(drop=True)
    df2.reset_index(drop=True)

    for idx in df1.index:
        if df1["Website"][idx] is None and df2["Website"][idx] is not None:
            df1["Website"][idx] = df2["Website"][idx]


if __name__ == "__main__":
    # First we add as many urls to our database in anyway we know how
    urls_to_add = extract_urls_from_emails(data)
    urls_to_add.append(extract_urls_from_web())
    # # Merge the two data frames so they have all the urls
    
    # # Here we need to clean the urls, ensuring they match regex and have a status code of 200

    # # Once we have MAX possible urls, we may start extracting data
    possible_new_emails = extract_emails_from_urls(data)


