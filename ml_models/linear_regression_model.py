import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from Vizualization.RegressionVizualization import *


def test_different_inputs(df, feature):
    """
    Given a dataframe and a feature, evaluate the model with different random_state values
    :param df:
    :param feature:
    :return:
    """
    for i in range(50):
        X = df[feature].values
        y = df['manually_checked'].values

        # train/split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=i)

        # create model
        model = LogisticRegression()

        # fit model to train data
        model.fit(X_train, y_train)

        # predict test/train
        y_pred_test = model.predict(X_test)
        y_pred_train = model.predict(X_train)

        # get r^2 score for train/test
        train_score = r2_score(y_train, y_pred_train)
        test_score = r2_score(y_test, y_pred_test)

        # predict the output given the features
        y_pred = model.predict(X)
        # calc Mean Average Error and Mean Squared Error
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)

        # Call visualization and load them into save_image()
        visualize_line_of_best_fit(X_test, y_test, y_pred_test, model, feature)
        plot_logistic_regression_plot(model, X, y)

        # print data (change to update a df)
        print("Model tested with feature {0} random_state: {1}".format(feature, i))
        print("R_2 (train): {0} | R_2 (test): {1}".format(train_score, test_score))
        print("MSE: {0} | MAE {1}".format(mse, mae))
        print("")


if __name__ == "__main__":

    df = pd.read_csv('/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSPROJECT1/BBB/data/filled_ind_var.csv')

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

    test_different_inputs(df, variables)


