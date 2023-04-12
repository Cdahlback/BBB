import csv
import random

import pandas as pd
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from ml_models.Vizualization.ClassificationVisualization import *

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from time import time


def test_eval(model, variables, r_s):

    # Create features and output
    X = data[variables].values
    y = data['manually_checked'].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=r_s)

    # Create a decision tree classifier
    clf = model

    # Train the classifier on the training data
    clf.fit(X_train, y_train)

    # Use the trained classifier to make predictions on the test data
    y_pred = clf.predict(X_test)

    # display confusion matrix and ROC curve
    print(model.__class__.__name__)
    display_confusion_matrix(y_test, y_pred)
    display_roc_curve(clf, X_train, y_train, X_test, y_test)

    # Measure the accuracy of the classifier
    accuracy = accuracy_score(y_test, y_pred)

    # save results
    print(f"Accuracy: {accuracy}")
    dict_to_append = {"Accuracy" : accuracy, "VariablesUsed" : variables[:], "RandomStateUsed" : r_s}
    add_to_csv(dict_to_append)

    # show and save decision tree
    # fig, ax = plt.subplots(figsize=(15, 15))
    # tree.plot_tree(clf, ax=ax)
    # plt.show()

    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(clf,
                       feature_names=variables,
                       class_names="manually_checked",
                       filled=True)
    plt.show()


def add_to_csv(dictionary):
    ml_stats_df.loc[len(ml_stats_df.index)] = dictionary


def get_highest_accuracy():
    """Gets the top5 largest accuracies from testing different inputs"""
    df = pd.read_csv("../data/ml_data/ml_stats.csv")
    new_df = df.loc[df["Accuracy"] >= .7]
    new_df.to_csv("../data/top_preformers.csv")


def get_feature_importance(clf, variables):
    """Code block used to compute feature importance"""
    # Compute feature importance
    importances = clf.feature_importances_

    # Print the feature importances
    for feature, importance in zip(variables, importances):
        print(f"{feature}: {importance:.3f}")


def test_diff_inputs(model, n, vars):
    """Code block to test different random_states and save results to a csv"""
    for i in range(0, n):
        test_eval(model, vars, i)
    ml_stats_df.to_csv("../data/ml_stats.csv")


if __name__ == "__main__":
    models = [DecisionTreeClassifier(max_depth=3),
              DecisionTreeClassifier(max_depth=6),
              ]

    data = pd.read_csv("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSPROJECT1/BBB/data/filled_ind_var.csv")
    ml_stats_df = pd.read_csv("../data/ml_data/ml_stats.csv")

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

    test_eval(models[1], variables, 0)

