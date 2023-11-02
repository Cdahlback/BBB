import time

import numpy as np
import requests
from bs4 import BeautifulSoup
from Extract_Data.data_extraction import *

"""Script to run our independent variable scrapers for entire database"""


def add_ind_var_columns(data):
    """
    A function that takes a DataFrame 'data' and adds several columns with boolean values
    :param data: data that is associated with Business URLS.
    :return: the modified DataFrame with the new columns added.
    """
    data["contains_contacts_page"] = np.nan
    data["contains_business_name"] = np.nan
    data["contains_business_name_in_copyright"] = np.nan
    data["contains_social_media_links"] = np.nan
    data["contains_reviews_page"] = np.nan
    data["contains_zipCode"] = np.nan
    data["url_contains_phone_number"] = np.nan
    data["url_is_review_page"] = np.nan
    return data


def fill_single_row(row):
    """
    A function to fill in a single row with information scraped from the Business URL.
    :param row: a row from a dataframe
    :return: updated row will proper information filled out
    """
    row = add_ind_var_columns(row)
    html = get_html(row["Website"])
    if html is None:
        print("not found")
        row["contains_contacts_page"] = False
        row["contains_business_name"] = False
        row["contains_business_name_in_copyright"] = False
        row["contains_social_media_links"] = False
        row["contains_reviews_page"] = False
        row["contains_zipCode"] = False
        row["url_contains_phone_number"] = False
        row["url_is_review_page"] = False
    else:
        business_name = row["BusinessName"]
        zip = row["PostalCode"]
        phone_number = row["Phone"]
        row["contains_contacts_page"] = contains_contacts_page(html)
        row["contains_business_name"] = contains_business_name(html, business_name)
        row[
            "contains_business_name_in_copyright"
        ] = contains_business_name_in_copyright(html, business_name)
        row["contains_social_media_links"] = contains_social_media_links(html)
        row["contains_reviews_page"] = contains_reviews_page(html)
        row["contains_zipCode"] = contains_zipCode(html, str(zip))
        row["url_contains_phone_number"] = contains_phone_number(
            html, str(phone_number)
        )
        row["url_is_review_page"] = url_is_review_page(row["Website"])


def fill_columns(data):
    """
    A function to fill in the new columns  with information scraped from the Business URL.
    :param data: data that is associated with the Business URLS.
    :return: cope of the data with new columns added.
    """
    data_copy = data.copy(deep=True)
    # t0 = time.time()

    # for index, row in data_copy.iterrows():
    website = data["Website"] if data["Website"] else None
    if pd.isnull(website):
        print("no website")
        return data_copy
    html = get_html(website)
    # print(index)
    if html is None:
        print("not found")
        data_copy.loc["contains_contacts_page"] = False
        data_copy.loc["contains_business_name"] = False
        data_copy.loc["contains_business_name_in_copyright"] = False
        data_copy.loc["contains_social_media_links"] = False
        data_copy.loc["contains_reviews_page"] = False
        data_copy.loc["contains_zipCode"] = False
        data_copy.loc["url_contains_phone_number"] = False
        # data_copy.loc[index, "url_contains_email"] = False
        data_copy.loc["url_is_review_page"] = False
        return data_copy
    else:
        business_name = data["BusinessName"]
        zip = data["PostalCode"]
        phone_number = data["Phone"]
        email = data["Email"]
        data_copy.loc["contains_contacts_page"] = contains_contacts_page(html)
        data_copy.loc["contains_business_name"] = contains_business_name(
            html, business_name
        )
        data_copy.loc[
            "contains_business_name_in_copyright"
        ] = contains_business_name_in_copyright(html, business_name)
        data_copy.loc["contains_social_media_links"] = contains_social_media_links(html)
        data_copy.loc["contains_reviews_page"] = contains_reviews_page(html)
        data_copy.loc["contains_zipCode"] = contains_zipCode(html, str(zip))
        data_copy.loc["url_contains_phone_number"] = contains_phone_number(
            html, str(phone_number)
        )
        # data_copy.loc[index, "url_contains_email"] = contains_email(html, email)
        data_copy.loc["url_is_review_page"] = url_is_review_page(website)
        # print("time taken to scrape ind vars for index: {0}".format(index))

    # t1 = time.time() - t0
    # print(t1)
    return data_copy


def get_html(website):
    """
    A function
    :param website: The URL of the website to retrieve the HTML from.
    :return: The HTML content of the page
    """
    if website is None:
        return None
    try:
        website = str(website)
        response = requests.get(website, timeout=7)
        html = BeautifulSoup(response.content, "html.parser")
        return html
    except Exception as e:
        return None


if __name__ == "__main__":
    df = pd.read_csv("/Users/jacksonthoe/Documents/GitHub/BBB/data/combined_data.csv")
    revised = add_ind_var_columns(df)
    final = fill_columns(revised)
    final.to_csv("/Users/jacksonthoe/Documents/GitHub/BBB/data/filled_ind_var.csv")
