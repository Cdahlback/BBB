import pickle

from ml_models.Vizualization.ClassificationVisualization import *
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Load the iris dataset
model_data = pd.read_csv("../data/filled_ind_var.csv")
ml_stats_df = pd.read_csv("../data/ml_data/ml_stats.csv")


def build_tree(input_data):
    """
    build decision tree based on data given
    :return trained model
    """
    # EDIT FEATURES HERE
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
        "IsBBBAccredited",
        "url_is_review_page",
    ]

    # Enter model data here:
    max_depth = 4
    ccp_alpha = 0

    # Create features and output (these should be created from the passed in dataframe, not the one stored locally here)
    X = input_data[features].values
    y = input_data["manually_checked"].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=0
    )

    # Create a decision tree classifier
    model = DecisionTreeClassifier(max_depth=max_depth, ccp_alpha=ccp_alpha)

    # Train the classifier on the training data
    model.fit(X_train, y_train)

    return model


def model_eval(model, variables, r_s):
    # Create features and output
    X = model_data[variables].values
    y = model_data["manually_checked"].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=r_s
    )

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
    dict_to_append = {
        "Accuracy": accuracy,
        "VariablesUsed": variables[:],
        "RandomStateUsed": r_s,
    }
    add_to_csv(dict_to_append)

    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(
        clf, feature_names=variables, class_names="manually_checked", filled=True
    )
    plt.show()


def add_to_csv(dictionary):
    ml_stats_df.loc[len(ml_stats_df.index)] = dictionary


def get_highest_accuracy():
    """Gets the top5 largest accuracies from testing different inputs"""
    df = pd.read_csv("../data/ml_data/ml_stats.csv")
    new_df = df.loc[df["Accuracy"] >= 0.7]
    new_df.to_csv("../data/top_preformers.csv")


def get_feature_importance(clf, variables):
    """Code block used to compute feature importance"""
    # Compute feature importance
    importance = clf.feature_importances_

    # Print the feature importance
    for feature, importance in zip(variables, importance):
        print(f"{feature}: {importance:.3f}")


def model_test_diff_inputs(model, n, vars):
    """Code block to test different random_states and save results to a csv"""
    for i in range(0, n):
        model_eval(model, vars, i)
    ml_stats_df.to_csv("../data/ml_stats.csv")


if __name__ == "__main__":
    model = build_tree(model_data)
    # store model into a pickle file
    with open("../ml_models/dt_model.pkl", "wb") as f:
        pickle.dump(model, f)
        f.close()
