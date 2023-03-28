from Extract_Data.create_urls import build_url_from_email
from Not_Our_Code.get_status_codes import get_statuscode
from Extract_Data.data_extraction import extract_email_data
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

    # Iterate over rows of our successful_urls (urls which were extracted from emails and given a status code
    for index, row in successful_urls.iterrows():
        # if that row is missing the website
        if pd.isnull(data.loc[index, "Website"]):
            # update the row with what we built
            data.loc[index, "Website"] = row['Website']
            data.loc[index, 'status_code'] = int(row['status_code'])
            data.loc[index, "found_via"] = "email"

    data = data.loc[(data['status_code'].isin([200, 403]))]
    return data


def add_found_via_column(data):
    """
    Adds the found_via column to the dataset
    :param data: original dataset
    :return:
    """
    data['FoundVia'] = ''

    has_URL = data.loc[data['Website'].notna()]
    has_URL['FoundVia'] = "BBB"

    has_Email = data.loc[data['Email'].notna() & data['Website'].isna()]
    has_Email['FoundVia'] = "Email"

    has_Neither = data.loc[data['Email'].isna() & data['Website'].isna()]
    has_Neither['FoundVia'] = 'Search'

    frames = [has_URL, has_Email, has_Neither]
    mn_bbb_businesses_foundVia = pd.concat(frames)
    compiled = mn_bbb_businesses_foundVia.reset_index(drop=True)

    # We will want to change this so it just returns the data with a new column
    compiled.to_csv('data/mn_bbb_businesses_foundVia.csv')
    return compiled


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
    df = pd.read_csv("../data/mn_bbb_businesses.csv", low_memory=False)
    # Add all found URLs from cells with emails
    # Add all found URLs from searching the web

    # Once we have MAX possible urls, we may start extracting data

