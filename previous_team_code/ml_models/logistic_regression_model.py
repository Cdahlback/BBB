import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from Vizualization.RegressionVizualization import *


def test_different_inputs(df, feature):
    """
    Given a dataframe and a feature, evaluate the model with different random_state values
    :param df:
    :param feature:
    :return:
    """

    X = df[feature].values
    y = df["manually_checked"].values

    # train/split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=21
    )

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

    # print data (change to update a df)
    print("Model tested with feature {0} random_state: {1}".format(feature, 21))
    print("R_2 (train): {0} | R_2 (test): {1}".format(train_score, test_score))
    print("MSE: {0} | MAE {1}".format(mse, mae))
    print("")

    # store model into a pickle file
    with open("../ml_models/lr_model.pkl", "wb") as f:
        pickle.dump(model, f)
        f.close()


if __name__ == "__main__":

    df = pd.read_csv("../Extract_Data/best_ind_vars.csv", low_memory=False)
    # EDIT VARIABLES HERE
    variables = [
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

    test_different_inputs(df, variables)
