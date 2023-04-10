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
    "/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSPROJECT1/BBB/data/filled_ind_var.csv")

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

def main_ml(data):
    # READ THE CSV THAT HAD JUST RAN THROUGH THE IND VAR SCRAPERS
    # NOTE: This data should have the following properties
    # 1. As many rows as the original dataframe
    # 2. All ind var columns filled out
    data = data.head(5)
    data['Accuracy'] = None
    for index, row in data.iterrows():
        if can_predict(row):
            selected_columns = np.array(row[variables]).reshape(1,-1)
            # Use the trained classifier to make predictions on the test data
            # in this case its just predicting one row
            y_pred = clf.predict(selected_columns)

            row['Predicted'] = y_pred
        else:
            row['Predicted'] = -1
        data.loc[index] = row
    # should have a dataset with no missing values for "Accuracy"
    return data


def can_predict(row):
    """
    We can predict a row if the following hold
    1. the url exists
    2. the url was found via search or email"""
    if _url_exists(row['Website']) and _not_found_via_bbb(row):
        return True
    # if the url doesn't exist or it was found via bbb, return false
    return False


def _url_exists(url):
    """Helper function for can_predict"""
    if url:
        return True
    else:
        return False


def _not_found_via_bbb(row):
    """Helper function for can_predict"""
    if row['FoundVia'] == "BBB":
        return False
    return True


if __name__ == "__main__":
    new_df = main_ml(data)
    print(new_df)