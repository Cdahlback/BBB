import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


def vizualize_compare_true_and_pred(y_test, y_pred_test):
    plt.scatter(y_test, y_pred_test)
    plt.xlabel("True Values")
    plt.ylabel("Predicted Values")

    m = y_test.min()
    M = y_test.max()

    plt.plot((m, M), (m, M), color='red')
    plt.show()


def visualize_line_of_best_fit(x_test, y_test, y_pred_test, model):
    plt.scatter(x_test, y_test)
    plt.plot(x_test, y_pred_test, color='red')
    plt.title("Model coef: {:0.3f}, Intercept: {:0.2f}".format(model.coef_[0], model.intercept_))
    plt.xlabel("Height")
    plt.ylabel("Weight");
    plt.show()


def visualize_feature_vs_dep_var(df, feature):
    # Possibly need to print
    sns.scatterplot(data=df,
                    x=feature,
                    y='manually_checked');
    plt.show()


def test_different_inputs(df, feature):
    for i in range(50):
        X = df[[feature]].values
        y = df['manually_checked'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=i)

        model = LinearRegression()

        model.fit(X_train, y_train)

        y_pred_test = model.predict(X_test)
        y_pred_train = model.predict(X_train)

        train_score = r2_score(y_train, y_pred_train)
        test_score = r2_score(y_test, y_pred_test)

        y_pred = model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)

        # Call visualization
        # vizualize_compare_true_and_pred(y_test, y_pred_test)
        # visualize_line_of_best_fit(X_test, y_test, y_pred_test, model)
        # visualize_feature_vs_dep_var(df, feature)

        # Create df from these values

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

    for variable in variables:
        test_different_inputs(df, variable)


