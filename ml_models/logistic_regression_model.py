import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# Read dataset
data = pd.read_csv("FILE HERE")

model_data = data[:1600]

holdout_data = data[1600:]

# Show correlation between variables
print(model_data.corr())

# Create Independent and Dependent variable sets
Y = model_data["manually_checked"].values

variables = ["contains_contacts_page",
             "contains_business_name",
             "contains_business_name_in_copyright",
             "contains_social_media_links",
             "contains_reviews_page"]

X = model_data[:, vars].values

# Split data into testing and training sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

# Building the model and fitting the data to it
website_relation_model = LogisticRegression()
website_relation_model.fit(x_train, y_train)

# Checking the predictive power of the model using the testing sets
y_prediction = website_relation_model.predict(x_test)

print()
print("Coefficients: \n", website_relation_model.coef_)

print("Root mean squared error: %.2f" % mean_squared_error(y_test, y_prediction, squared=False))

print("Coefficient of determination: %.2f" % r2_score(y_test, y_prediction))
