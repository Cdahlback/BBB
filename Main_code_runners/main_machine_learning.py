import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

"""
In the readME for this directory, find the section labeled MACHINE LEARNING for steps and suggestions for global
variable values. 
"""


# ###############################################--Global vars--#######################################################

# Here you can comment out features and try different permutations
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
        "IsBBBAccredited"
    ]


def main(df, df_copy):
    # Enter model data here:
    max_depth = 4
    ccp_alpha = 0

    # Create features and output (these should be created from the passed in dataframe, not the one stored locally here)
    X = df[features].values
    y = df['manually_checked'].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    # Create a decision tree classifier
    model = DecisionTreeClassifier(max_depth=max_depth, ccp_alpha=ccp_alpha)

    # Train the classifier on the training data
    model.fit(X_train, y_train)
    stream = {'BusinessID': None, 'Email': None, 'Phone': None, 'Website': None, "Addresses": None, 'predictive%': None}
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
        businessID = row['BusinessID']
        if can_predict(row):
            selected_columns = np.array(row[features]).reshape(1, -1)
            # in this case its just predicting one row
            y_pred = model.predict(selected_columns)

            # here we need to add the data to a stream, since we now have everything aquired.
            row_copy = data_copy.loc[data_copy['BusinessID'] == businessID]
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
    dict = {"BusinessID": businessID, "Website": None, "Emails": None, "PhoneNums": None, "Addresses": None,
            "PredictivePercentage": predictive_percentage}
    url = row['Website']
    dict["Website"] = url

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    if _new_email_found(row, row_copy):
        dict['Emails'] = row['Email']

    # check if we found a new phone number, if we did add it to the stream. (it is plural ATM due to a list of
    # emails being returned. possibly)
    if _new_phone_found(row, row_copy):
        dict['Phone'] = row['Phone']

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    if _new_address_found(row, row_copy):
        dict['Addresses'] = row['Address']

    stream.append(dict)


def _new_email_found(row, row_copy):
    """
    If there is no data in our original dataframe, and data in our updated dataframe, we have successfully found an email

    :param row: updated dataframe containing scraped data
    :param row_copy: original dataframe with no updated values
    :return:
    """
    # if there wasn't an email there already
    if pd.isnull(row_copy['Email']):
        if pd.notnull(row['Email']):
            return True
    # if there already was an email there, don't add it to the stream
    else:
        return False


def _new_phone_found(row, row_copy):
    """
    If there is no data in our original dataframe, and data in our updated dataframe, we have successfully found a phone

    :param row: updated dataframe containing scraped data
    :param row_copy: original dataframe with no updated values
    :return:
    """
    # if there wasn't a phone there already
    if pd.isnull(row_copy['Phone']):
        if pd.notnull(row['Phone']):
            return True
    # if there already was a phone there, don't add it to the stream
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
    if pd.isnull(row_copy['Address']):
        if pd.notnull(row['Address']):
            return True
    # if there already was an address there, don't add it to the stream
    else:
        return False


def can_predict(row):
    """
    helper function for main_ml
    determines if a row of data can be predicted
    """
    if _url_exists(row['Website']):
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
