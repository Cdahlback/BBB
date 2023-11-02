import pickle

import numpy as np
import pandas as pd
from Extract_Data.fill_ind_var_columns import fill_columns

"""
In the readME for this directory, find the section labeled MACHINE LEARNING for steps and suggestions for global
variable values. 
"""


# ###############################################--Global vars--#######################################################

features = [
    "contains_contacts_page",
    "contains_business_name",
    "contains_business_name_in_copyright",
    "contains_social_media_links",
    "contains_reviews_page",
    "contains_zipCode",
    "url_contains_phone_number",
    "BBBRatingScore",
    "IsHQ",
    "IsCharity",
    "IsBBBAccredited",
    "url_is_review_page",
]


def main(df, df_copy):
    # open decision tree model from pickle file
    with open("../ml_models/dt_model.pkl", "rb") as f:
        model = pickle.load(f)
        f.close()
    # create stream
    stream = pd.DataFrame(
        columns=["BusinessID", "Email", "Phone", "Website", "Addresses", "predictive%"]
    )
    return main_ml(df, df_copy, stream, model)


# ###############################################--FUNCTIONS--##########################################################


def main_ml(data, data_copy, stream, model):
    """
    MORE INFO IN readME for this directory.
    Used for two major functionality.
    1. Knowing if we should add a row of data to a stream
    2. Predicting the percentage of the website being associated with its business
    :param data: updated data, this should have new data scraped from the web
    :param data_copy: copy of original data, this should have NONE of the data we found
    :param stream: used to hold data we have added to BBBs dataframe, we expect this to be used for determining if a
                   row needs to be manually checked.
    :return: stream of data
    """
    for index, row in data.iterrows():
        businessID = row["BusinessID"]
        if can_predict(row):
            row = fill_columns(row)
            selected_columns = np.array(row[features]).reshape(1, -1)
            # in this case its just predicting one row
            y_pred = model.predict_proba(selected_columns)

            print("Predictions: ", y_pred)
            y_pred = y_pred[0][1]

            # here we need to add the data to a stream, since we now have everything aquired.
            row_copy = data_copy[data_copy["BusinessID"] == businessID]
            add_to_stream(row, row_copy, stream, y_pred)
    return stream


def add_to_stream(row, row_copy, stream, predictive_percentage):
    """
    This function assumes the url exists, it will never be called when a url doesn't exist, so therefor, this function
    will always add data to the stream.
    The idea of this function is to compare our updated dataframe to our copy, adding all new data we found to this stream
    :param predictive_percentage: passed in value for percentage
    :param row: row of the dataframe that has been updated
    :param row_copy: row of the dataframe that has not been updated
    :param stream: dataframe we need to update
    :return: None
    """
    businessID = row["BusinessID"]
    dict = {
        "BusinessID": businessID,
        "Email": None,
        "Phone": None,
        "Website": None,
        "Addresses": None,
        "predictive%": predictive_percentage,
    }
    url = row["Website"]
    dict["Website"] = url

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    if _new_email_found(row, row_copy, businessID):
        dict["Email"] = row["Email"]

    # check if we found a new phone number, if we did add it to the stream. (it is plural ATM due to a list of
    # emails being returned. possibly)
    if _new_phone_found(row, row_copy, businessID):
        dict["Phone"] = row["Phone"]

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    # if _new_address_found(row, row_copy, businessID):
    #     dict['Addresses'] = row['Address']

    series_dict = pd.Series(dict)
    stream.loc[len(stream)] = series_dict


def _new_email_found(row, row_copy, businessId):
    """
    If there is no data in our original dataframe, and data in our updated dataframe, we have successfully found an email
    :param row: updated dataframe containing scraped data
    :param row_copy: original dataframe with no updated values
    :return:
    """
    possible_new_email = row["Email"]
    old_value = row_copy.loc[row_copy["BusinessID"] == businessId, "Email"].iloc[0]
    if isinstance(possible_new_email, list) and pd.isna(old_value):
        return True
    if pd.notna(possible_new_email) and pd.isna(old_value):
        return True
    else:
        return False


def _new_phone_found(row, row_copy, businessId):
    """
    If there is no data in our original dataframe, and data in our updated dataframe, we have successfully found a phone
    :param row: updated dataframe containing scraped data
    :param row_copy: original dataframe with no updated values
    :return:
    """
    possible_new_phone = row["Phone"]
    old_value = row_copy.loc[row_copy["BusinessID"] == businessId, "Email"].iloc[0]
    if isinstance(possible_new_phone, list) and pd.isna(old_value):
        return True
    if pd.notna(possible_new_phone) and pd.isna(old_value):
        return True
    else:
        return False


def _new_address_found(row, row_copy):
    """
    If there is no data in our original dataframe, and data in our updated dataframe, we have successfully found an address
    :param row: updated dataframe containing scraped data
    :param row_copy: original dataframe with no updated values
    :return:
    """
    # if there wasn't an address there already
    if row_copy["Address"].empty:
        if row["Address"].empty:
            return True
    # if there already was an address there, don't add it to the stream
    else:
        return False


def can_predict(row):
    """
    helper function for main_ml
    determines if a row of data can be predicted
    """
    if _url_exists(row["Website"]):
        return True
    # if the url doesn't exist, return false, since we cannot predict anything
    return False


def _url_exists(url):
    """
    Checks if this row has a url
    if we have a url, return True.
    if we dont have a url, return false.
    """
    if url:
        return True
    else:
        return False
