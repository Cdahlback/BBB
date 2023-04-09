import time
import pandas as pd
import numpy as np
from data_extraction import *
import requests
from bs4 import BeautifulSoup


def add_ind_var_columns(data):
    """
    A function that takes a DataFrame 'data' and adds several columns with boolean values
    :param data: data that is associated with Business URLS.
    :return: the modified DataFrame with the new columns added.
    """
    columns = ['contains_contacts_page', 'contains_business_name', 'contains_business_name_in_copyright',
               'contains_social_media_links', 'contains_reviews_page', 'contains_zipCode',
               'url_contains_phone_number', 'url_contains_email', 'url_is_review_page']
    data[columns] = False
    return data


def fill_columns(data):
    """
    A function to fill in the new columns with information scraped from the Business URL.
    :param data: data that is associated with the Business URLS.
    :return: copy of the data with new columns added.
    """
    data_copy = data.copy(deep=True)
    t0 = time.time()

    for index, row in data_copy.iterrows():
        website = row["Website"]
        html = get_html(website)
        if html is None:
            continue

        data_copy.loc[index, "contains_contacts_page"] = contains_contacts_page(html)
        data_copy.loc[index, "contains_business_name"] = contains_business_name(html, row["BusinessName"])
        data_copy.loc[index, "contains_business_name_in_copyright"] = contains_business_name_in_copyright(
            html, row["BusinessName"])
        data_copy.loc[index, "contains_social_media_links"] = contains_social_media_links(html)
        data_copy.loc[index, "contains_reviews_page"] = contains_reviews_page(html)
        data_copy.loc[index, "contains_zipCode"] = contains_zipCode(html, row["PostalCode"])
        data_copy.loc[index, "url_contains_phone_number"] = contains_phone_number(html, row["Phone"])
        data_copy.loc[index, "url_contains_email"] = contains_email(html, "Email")
        data_copy.loc[index, "url_is_review_page"] = contains_reviews_page(html)

    t1 = time.time() - t0
    print(f"Elapsed time: {t1:.2f} seconds.")
    return data_copy


def get_html(website):
    """
    A function that retrieves the HTML content of a webpage.
    :param website: The URL of the website to retrieve the HTML from.
    :return: The HTML content of the page, or None if an error occurs.
    """
    if pd.isnull(website):
        return None
    try:
        response = requests.get(website, timeout=7)
        html = BeautifulSoup(response.content, 'html.parser')
        return html
    except:
        return None


if __name__ == '__main__':
    input = pd.read_csv('../data/combined_data.csv')
    revised = add_ind_var_columns(input)
    final = fill_columns(revised)
    final.to_csv('../data/filled_ind_var2.csv')


