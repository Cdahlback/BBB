import time
from data_extraction import *
import numpy as np
import requests
from bs4 import BeautifulSoup


"""Script to run our independent variable scrapers for entire database"""


def add_ind_var_columns(data):
    """
    A function that takes a DataFrame 'data' and adds several columns with boolean values
    :param data: data that is associated with website URL's.
    :return: the modified DataFrame with the new columns added.
    """
    data['contains_contacts_page'] = np.nan
    data['contains_business_name'] = np.nan
    data['contains_business_name_in_copyright'] = np.nan
    data['contains_social_media_links'] = np.nan
    data['contains_reviews_page'] = np.nan
    data['contains_zipCode'] = np.nan
    data['url_contains_phone_number'] = np.nan
    data['url_contains_email'] = np.nan
    return data


def fill_columns(data):
    """
    A function
    """
    data_copy = data.copy(deep=True)
    data_copy = data_copy.iloc[:500,:]
    t0 = time.time()
    for index, row in data_copy.iterrows():
        website = row["Website"] if row["Website"] else None
        if pd.isnull(website):
            continue
        t2 = time.time()
        html = get_html(website)
        print(time.time() - t2)
        if html is None:
            print("not found")
            continue
        elif pd.isnull(row["Email"]):
            continue
        else:
            business_name = row["BusinessName"]
            zip = row["PostalCode"]
            phone_number = row["Phone"]
            email = row["Email"]
            row_idx = data.index[data['BusinessName'] == business_name].tolist()
            data_copy.loc[row_idx[0], "contains_contacts_page"] = contains_contacts_page(html)
            data_copy.loc[row_idx[0], "contains_business_name"] = contains_business_name(html, business_name)
            data_copy.loc[row_idx[0], "contains_business_name_in_copyright"] = contains_business_name_in_copyright(html, business_name)
            data_copy.loc[row_idx[0], "contains_social_media_links"] = contains_social_media_links(html)
            data_copy.loc[row_idx[0], "contains_reviews_page"] = contains_reviews_page(html)
            data_copy.loc[row_idx[0], "contains_zipCode"] = contains_zipCode(html, zip)
            data_copy.loc[row_idx[0], "url_contains_phone_number"] = url_contains_phone_number(html, phone_number)
            data_copy.loc[row_idx[0], "url_contains_email"] = url_contains_email(html, email)

    t1 = time.time() - t0
    print(t1)
    return data_copy


def get_html(website):
    if website is None:
        return None
    try:
        website = str(website)
        response = requests.get(website, timeout=7)
        html = BeautifulSoup(response.content, 'html.parser')
        return html
    except Exception as e:
        return None

