import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

"""This file is used for encapsulating all necessary information needed to predict a specific row of a dataframe

It must:
- Add a column named "Accuracy"
- Assign a accuracy for each specific row, if the url was already provided by bbb mark this as -1"""


# ###############################################--Global vars--#######################################################

data = pd.read_csv(
    "../data/filled_ind_var.csv")

# Once feature selection is done we can change these to the strongest predictors
variables = [
    "contains_contacts_page",
    "contains_business_name",
    "contains_business_name_in_copyright",
    "contains_social_media_links",
    "contains_reviews_page",
    "contains_zipCode",
    "url_contains_email",
    "url_contains_phone_number",
    "BBBRatingScore",
    "IsHQ",
    "IsCharity",
    "IsBBBAccredited"
]

# Create features and output
X = data[variables].values
y = data['manually_checked'].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Create a decision tree classifier
clf = DecisionTreeClassifier()

# Train the classifier on the training data
clf.fit(X_train, y_train)


# ###############################################--FUNCTIONS--##########################################################

def main_ml(data, data_copy, stream):
    """
    Used for two major functionallity.
    1. Knowing if we should add a row of data to a stream
    2. Predicting the likely-hood of the website being associated with its business
    :param data: updated data, this should have new data scraped from the web
    :param data_copy: copy of original data, this should have NONE of the data we found
    :param stream: used to hold data we have added to BBBs dataframe, we expect this to be used for determining if a
                   row needs to be manually checked.
    :return: stream of data
    """
    for index, row in data.iterrows():
        businessID = row['BusinessID']
        if can_predict(row):
            selected_columns = np.array(row[variables]).reshape(1,-1)
            # in this case its just predicting one row
            y_pred = clf.predict(selected_columns)

            # here we need to add the data to a stream, since we now have everything aquired.
            row_copy = data_copy.loc[data_copy['BusinessID'] == businessID]
            add_to_stream(row, row_copy, stream, y_pred)
    return stream


def add_to_stream(row, row_copy, stream, predictive_percentage):
    """
    This function assumes the url exists, it will never be called when a url doesn't exist, so therefor, this function
    will always add data to the stream.
    The idea of this function is to compare our updated dataframe to our copy, adding all new data we found to this stream
    :param row: row of the dataframe that has been updated
    :param row_copy: row of the dataframe that has not been updated
    :param stream: dataframe we need to update
    :return:
    """
    businessID = row["BusinessID"]
    dict = {"BusinessID": businessID, "Url": None, "Emails": None, "PhoneNums": None, "Addresses": None,
            "PredictivePercentage": predictive_percentage}
    url = row['Website']
    dict["Url"] = url

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    if _new_email_found(row, row_copy):
        emails = row['Email']
        dict['Emails'] = emails

    # check if we found a new phone number, if we did add it to the stream. (it is plural ATM due to a list of
    # emails being returned. possibly)
    if _new_phone_found(row, row_copy):
        phone = row['Phone']
        dict['Phone'] = phone

    # check if we found a new email, if we did add it to the stream. (it is plural ATM due to a list of emails
    # being returned. possibly)
    if _new_address_found(row, row_copy):
        address = row['Address']
        dict['Addresses'] = address

    stream.append(dict)


def _new_email_found(row, row_copy):
    # if there wasn't an email there already
    if pd.isnull(row_copy['Email']):
        if pd.notnull(row['Email']):
            return True
    # if there already was an email there, don't add it to the stream
    else:
        return False


def _new_phone_found(row, row_copy):
    # if there wasn't a phone there already
    if pd.isnull(row_copy['Phone']):
        if pd.notnull(row['Phone']):
            return True
    # if there already was a phone there, don't add it to the stream
    else:
        return False


def _new_address_found(row, row_copy):
    # if there wasn't an address there already
    if pd.isnull(row_copy['Address']):
        if pd.notnull(row['Address']):
            return True
    # if there already was an address there, don't add it to the stream
    else:
        return False


def can_predict(row):
    """
    We can predict a row if the following hold
    1. the url exists
    2. the url was found via search or email"""
    if _url_exists(row['Website']):
        return True
    # if the url doesn't exist, return false, since we cannot predict anything
    return False


def _url_exists(url):
    """Helper function for can_predict"""
    if url:
        return True
    else:
        return False


if __name__ == "__main__":
    new_df = main_ml(data)
    print(new_df)