from create_urls import build_url_from_email
from Not_Our_Code.get_status_codes import get_statuscode, status_code
from data_extraction import extract_email_data, extract_phone_data
from fill_ind_var_columns import fill_columns
from time import time
import numpy as np
import pandas as pd


def extract_urls_from_emails(data):
    """
    Function to create urls from email domains.
    :param data: passed in dataframe from main
    :return: New DataFrame with columns BusinessID, Website.
    """
    emails_no_url = data.copy(deep=True)
    emails_no_url = emails_no_url.loc[(data['Email'].notna()) & (data['Website'].isna())][['BusinessID', 'Email']]

    # extract URLs for all emails without urls
    emails_no_url["Website"] = emails_no_url['Email'].apply(lambda email: build_url_from_email(email))
    successful_urls = emails_no_url.copy(deep=True)
    successful_urls = successful_urls.loc[successful_urls['Website'].notna()]
    # .to_list()
    status_code_df = get_statuscode(successful_urls["Website"])
    successful_urls["status_code"] = status_code_df

    # merge the two df
    # Logic to merge:
    # Only update if the website cell is null
    for index, row in successful_urls.iterrows():
        # Extract info to merge into data
        status_code = row["status_code"]
        url_extracted = row["Website"]
        business_id = row["BusinessID"]
        # find index of row with possible missing value
        col_idx_website = data.columns.get_loc("Website")
        col_idx_found_via = data.columns.get_loc("found_via")
        # if that row is missing the website (11 is the column index of website)
        if pd.isnull(data.loc[index, "Website"]):
            data.loc[index, "Website"] = url_extracted
            data.loc[index, 'status_code'] = int(status_code)
            data.loc[index, "found_via"] = "email"

    # data = data.loc[(data['status_code'] == 200)]
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


if __name__ == "__main__":
    df = pd.read_csv("data/mn_bbb_businesses.csv", low_memory=False)
    df['found_via'] = np.nan
    # Add all found URLs from cells with emails
    df = extract_urls_from_emails(df.iloc[:5000,:])
    # Add all found URLs from searching the web
    # extract_urls_from_search(df)

    # Fill columns for independent variables
    df = fill_columns(df)
    print(df)

    # Once we have MAX possible urls, we may start extracting data

