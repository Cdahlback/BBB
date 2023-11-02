import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


def vizualize_compare_true_and_pred(y_test, y_pred_test):
    """
    Scatter plot to compare true vs predicted values
    :param y_test: actual true data
    :param y_pred_test: predicted data
    :return: plot for saving to a pdf
    """
    plt.scatter(y_test, y_pred_test)
    plt.title("True vs Pred")
    plt.xlabel("True Values")
    plt.ylabel("Predicted Values")

    m = y_test.min()
    M = y_test.max()

    plt.plot((m, M), (m, M), color="red")
    return plt


def visualize_line_of_best_fit(x_test, y_test, y_pred_test, model, feature):
    """
    Linear line of best fit
    :param x_test: feature test data
    :param y_test: output test data (true)
    :param y_pred_test: output test data (pred)
    :param model: model used for plot
    :param feature: feature name used (Only takes in one feature)
    :return:
    """
    plt.scatter(x_test, y_test)
    plt.plot(x_test, y_pred_test, color="red")
    plt.title("Line of best fit")
    plt.title(
        "Model coef: {:0.3f}, Intercept: {:0.2f}".format(
            model.coef_[0], model.intercept_
        )
    )
    plt.xlabel(feature)
    plt.ylabel("manually_checked")
    return plt


def visualize_feature_vs_dep_var(df, feature):
    """
    Compare feature vs dep_var in scatter plot
    :param df:
    :param feature: name of feature
    :return:
    """
    # Possibly need to print
    sns.scatterplot(data=df, x=feature, y="manually_checked")
    plt.title("feature vs dep var")
    return plt


def save_image(filename):
    """
    Used to save our plots to pdfs
    :param filename: filename we want to save it as
    :return:
    """
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
        fig.savefig(p, format="pdf")

        # close the object
    p.close()


def plot_logistic_regression_bar(model, feature):
    """
    Plot logistic regression bar chart
    :param model:
    :param feature:
    :return:
    """
    # Extract feature names and coefficients
    coefficients = model.coef_[0]

    # Create a DataFrame of coefficients
    coef_df = pd.DataFrame({"feature": feature, "coefficient": coefficients})

    # Create a bar chart of coefficients
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x="coefficient", y="feature", data=coef_df, orient="h", ax=ax)
    ax.set_title("Logistic Regression Coefficients")
    ax.set_xlabel("Coefficient")
    ax.set_ylabel("Feature")
    return plt


def plot_logistic_regression_plot(model, X, y):
    """
    Plot logistic regression plot
    :param model:
    :param X: Feature column(s)
    :param y: Dev var column
    :return:
    """
    # Create a logistic regression plot
    fig, ax = plt.subplots(figsize=(8, 6))
    x = model.predict_proba(X)[:, 1]
    sns.regplot(x=model.predict_proba(X)[:, 1], y=y, logistic=True, ax=ax)
    ax.set_title("Logistic Regression Plot")
    ax.set_xlabel("Predicted Probability")
    ax.set_ylabel("Actual Outcome")
    return plt
