import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Read in the CSV file as a Pandas DataFrame
data = pd.read_csv("../data/filled_ind_var.csv", low_memory=False)

# Select the input variables
input_vars = ["IsBBBAccredited", "BBBRatingScore", "NumberOfEmployees", "contains_contacts_page", "contains_business_name", "contains_social_media_links", "contains_reviews_page", "contains_zipCode"]

# Split the data into training and testing sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Create a Decision Tree Classifier model
model = DecisionTreeClassifier(random_state=42)

# Train the model on the training data
model.fit(train_data.drop("BusinessID", axis=1), train_data["input_vars"])

# Make predictions on the test data
predictions = model.predict(test_data.drop("BusinessID", axis=1))

# Calculate the accuracy of the model
accuracy = accuracy_score(test_data["input_vars"], predictions)

# Print the accuracy of the model
print("Model accuracy: {:.2f}%".format(accuracy * 100))

# Export the decision tree as a DOT file
export_graphviz(model, out_file="tree.dot", feature_names=train_data.drop(["BusinessID"], axis=1).columns, filled=True, rounded=True, special_characters=True)

# Convert the DOT file to a PNG image using the Graphviz software
import os
os.system("dot -Tpng tree2.dot -o tree2.png")
