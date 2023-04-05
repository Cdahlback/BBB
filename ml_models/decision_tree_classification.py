import pandas as pd
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import graphviz
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'


# Load the iris dataset
data = pd.read_csv("../data/filled_ind_var.csv")

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

# Create a decision tree classifier with max_depth=3
clf = DecisionTreeClassifier(max_depth=3)

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Use the trained classifier to make predictions on the test data
y_pred = clf.predict(X_test)

# Measure the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

dot_data = export_graphviz(clf, out_file=None,
                           feature_names=variables,
                           class_names=['0', '1'],
                           filled=True, rounded=True,
                           special_characters=True, max_depth=3)#will show only 3 depth
graph = graphviz.Source(dot_data)
graph.render('decision_tree', format='png', view=True)

