import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


def vizualize_compare_true_and_pred(y_test, y_pred_test):
    plt.scatter(y_test, y_pred_test)
    plt.title("True vs Pred")
    plt.xlabel("True Values")
    plt.ylabel("Predicted Values")

    m = y_test.min()
    M = y_test.max()

    plt.plot((m, M), (m, M), color='red')
    return plt


def visualize_line_of_best_fit(x_test, y_test, y_pred_test, model, feature):
    plt.scatter(x_test, y_test)
    plt.plot(x_test, y_pred_test, color='red')
    plt.title("Line of best fit")
    plt.title("Model coef: {:0.3f}, Intercept: {:0.2f}".format(model.coef_[0], model.intercept_))
    plt.xlabel(feature)
    plt.ylabel("manually_checked");
    return plt


def visualize_feature_vs_dep_var(df, feature):
    # Possibly need to print
    sns.scatterplot(data=df,
                    x=feature,
                    y='manually_checked')
    plt.title("feature vs dep var")
    return plt


def save_image(filename):
    # PdfPages is a wrapper around pdf
    # file so there is no clash and create
    # files with no error.
    p = PdfPages(filename)

    # get_fignums Return list of existing
    # figure numbers
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]

    # iterating over the numbers in list
    for fig in figs:
        # and saving the files
        fig.savefig(p, format='pdf')

        # close the object
    p.close()


def test_different_inputs(df, feature):
    for i in range(50):
        X = df[[feature]].values
        y = df['manually_checked'].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=i)

        model = LogisticRegression()

        model.fit(X_train, y_train)

        y_pred_test = model.predict(X_test)
        y_pred_train = model.predict(X_train)

        train_score = r2_score(y_train, y_pred_train)
        test_score = r2_score(y_test, y_pred_test)

        y_pred = model.predict(X)
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)

        # Call visualization
        plt1 = vizualize_compare_true_and_pred(y_test, y_pred_test)
        plt2 = visualize_line_of_best_fit(X_test, y_test, y_pred_test, model, feature)
        plt3 = visualize_feature_vs_dep_var(df, feature)
        plt4 = plot_logistic_regression_bar(model, feature)
        plt5 = plot_logistic_regression_plot(model, X, y)

        save_image("multi_plot_image.pdf")

        print("Model tested with feature {0} random_state: {1}".format(feature, i))
        print("R_2 (train): {0} | R_2 (test): {1}".format(train_score, test_score))
        print("MSE: {0} | MAE {1}".format(mse, mae))
        print("")


def plot_logistic_regression_bar(model, feature):
    # Extract feature names and coefficients
    coefficients = model.coef_[0]

    # Create a DataFrame of coefficients
    coef_df = pd.DataFrame({'feature': feature, 'coefficient': coefficients})

    # Create a bar chart of coefficients
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='coefficient', y='feature', data=coef_df, orient='h', ax=ax)
    ax.set_title('Logistic Regression Coefficients')
    ax.set_xlabel('Coefficient')
    ax.set_ylabel('Feature')
    return plt


def plot_logistic_regression_plot(model, X, y):
    # Create a logistic regression plot
    fig, ax = plt.subplots(figsize=(8, 6))
    x = model.predict_proba(X)[:, 1]
    sns.regplot(x=model.predict_proba(X)[:, 1], y=y, logistic=True, ax=ax)
    ax.set_title('Logistic Regression Plot')
    ax.set_xlabel('Predicted Probability')
    ax.set_ylabel('Actual Outcome')
    return plt


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


