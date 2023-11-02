import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def display_confusion_matrix(y_test, y_pred):

    cm = confusion_matrix(y_test, y_pred)

    x = pd.DataFrame(cm, index=["Miss", "Hit"], columns=["pred_Miss", "pred_Hit"])

    print(x.head())
    print(classification_report(y_test, y_pred))


import matplotlib.pyplot as plt
from sklearn.metrics import auc, roc_curve
from sklearn.tree import DecisionTreeClassifier


def display_roc_curve(clf, X_train, y_train, X_test, y_test):
    """
    Plots the ROC curve for a given decision tree classification model.

    Parameters:
    clf (DecisionTreeClassifier): the decision tree classification model
    X_train (array-like): the training input samples
    y_train (array-like): the target values for the training input samples
    X_test (array-like): the testing input samples
    y_test (array-like): the target values for the testing input samples

    Returns:
    None
    """

    # Train the model
    clf.fit(X_train, y_train)

    # Get predicted probabilities for the test set
    y_score = clf.predict_proba(X_test)[:, 1]

    # Compute the ROC curve and ROC area for each class
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_auc = auc(fpr, tpr)

    # Plot the ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(
        fpr, tpr, color="darkorange", lw=2, label="ROC curve (area = %0.2f)" % roc_auc
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.show()
