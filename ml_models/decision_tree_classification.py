import random

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ml_models.Vizualization.ClassificationVisualization import *

# Load the iris dataset

data = pd.read_csv("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSPROJECT1/BBB/data/filled_ind_var.csv")

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


def test_ipts_decision_tree(data, variables, r_s, ml_stats_df):

    # Create features and output
    X = data[variables].values
    y = data['manually_checked'].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=r_s)

    # Create a decision tree classifier
    clf = DecisionTreeClassifier()

    # Train the classifier on the training data
    clf.fit(X_train, y_train)

    # Use the trained classifier to make predictions on the test data
    y_pred = clf.predict(X_test)

    # display confusion matrix and ROC curve
    display_confusion_matrix(y_test, y_pred)
    # display_roc_curve(clf, X_train, y_train, X_test, y_test)

    # Measure the accuracy of the classifier
    accuracy = accuracy_score(y_test, y_pred)

    # save results
    dict_to_append = {"Accuracy" : accuracy, "VariablesUsed" : variables[:], "RandomStateUsed" : r_s}

    # concatenate the new DataFrame with the original DataFrame
    ml_stats_df.loc[len(ml_stats_df.index)] = dict_to_append
    return ml_stats_df


stats_df = pd.read_csv("../data/ml_stats.csv")
for i in range(50, 150):
    k = random.randint(1, len(variables))
    vars_used = random.sample(variables, k)
    stats_df = test_ipts_decision_tree(data, vars_used, i, stats_df)

stats_df.to_csv("../data/ml_stats.csv")