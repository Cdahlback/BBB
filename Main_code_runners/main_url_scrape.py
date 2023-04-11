from Extract_Data.create_urls import *
from Not_Our_Code.get_status_codes import *
import pandas as pd
import re

def main_scrape_urls(df):

    """
    Given a dataframe, adds any missing URLs found via email or web search and checks their status codes.
    If the status code is 200, updates the 'Website' column of the input dataframe with the valid URL.
    :param df: a pandas dataframe containing business information
    :return: the modified pandas dataframe
    """

    email_df = pd.DataFrame(columns=df.columns)
    search_df = pd.DataFrame(columns=df.columns)

    for index, row in df.iterrows():
        # Check if the row already has a valid URL
        bbb_df = check_website_column(row)
        # If it does, skip to the next row
        if index in bbb_df.index:
            continue

        website = url_from_email(row)

        # If a valid URL is found, add the row to the email results dataframe
        if website:
            row['Website'] = website
            email_df = email_df.append(row, ignore_index=True)
            # Otherwise, try to get a URL from the business name column using web search
        else:
            website = url_from_business_name(row)
            if website:
                row['Website'] = website
                search_df = search_df.append(row, ignore_index=True)

    bbb_df = pd.concat([email_df, search_df], ignore_index=True)   # Combine the email and search results into a single dataframe
    bbb_df = get_statuscode_forPandas(bbb_df)  # Check the status codes of the URLs

    # If the status code is 200, update the 'Website' column of the input dataframe with the valid URL
    for index, row in bbb_df.iterrows():
        status_code = row['Status Code']
        if status_code == 200:
            df.loc[index, 'Website'] = row['Website']
            # Otherwise, drop the row from the result dataframe
        else:
            bbb_df = bbb_df.drop(index)

    return df #modified DataFrame


def check_website_column(row):
    """
    Given a row, checks if the 'Website' column contains a URL.
    Returns the URL if it is valid, otherwise returns None.
    """

    website = row['Website']
    if isinstance(website, str) and re.match(r'^https?://', website):
        return website
    return None

def url_from_email(row):
    """
    Given a row, attempts to build a URL from the email column.
    Returns the URL if it is valid, otherwise returns None.
    """

    email = row['Email']
    if isinstance(email, str):
        website = build_url_from_email(email)
        if website:
            return website
        return None

def url_from_business_name(row):
    """
        Given a row, attempts to find a URL from the BusinessName column.
        Returns the URL if it is valid, otherwise returns None.
        """

    business_name = row['BusinessName']
    #add more
    if isinstance(business_name, str):
        website = search_urls(business_name)#get_url_from_search function
        if website:
            return website
    return None


if __name__ == '__main__':

    df = pd.read_csv('mn_bbb_businesses.csv')
    df = main_scrape_urls(df)
    df.to_csv('mn_bbb_businesses_with_urls.csv', index=False)