from create_urls import build_url_from_email
from Not_Our_Code.get_status_codes import get_statuscode, status_code
from data_extraction import extract_email_data, extract_phone_data
from time import time
import numpy as np
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
    status_code_df = get_statuscode(successful_urls["Website"].to_list())
    successful_urls["status_code"] = status_code_df
    data['status_code'] = np.nan
    data['found_via'] = np.nan

    # merge the two df
    # Logic to merge:
    # Only update if the website cell is null
    for row in successful_urls.iterrows():
        # Extract info to merge into data
        status_code = row[1]["status_code"]
        url_extracted = row[1]["Website"]
        business_id = row[1]["BusinessID"]
        # find index of row with possible missing value
        row_idx = data.index[data['BusinessID'] == business_id].tolist()
        if len(row_idx) > 1:
            print(row_idx)
        # if that row is missing the website (11 is the column index of website)
        if pd.isnull(data.iloc[row_idx[0], 11]):
            data.loc[row_idx[0], 11] = url_extracted
            data.loc[row_idx[0], 24] = int(status_code)
            data.loc[row_idx[0], 25] = "email"

    data = data.loc[(data['status_code'] < 300) & (data['status_code'] > 199)]
    return data


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
    df = pd.read_csv("data/mn_bbb_businesses.csv", low_memory=False)
    extract_urls_from_emails(df)


# First we add as many urls to our database in anyway we know how
    # df = extract_urls_from_emails(df)
    # df.append(extract_urls_from_web())

    # Once we have MAX possible urls, we may start extracting data

