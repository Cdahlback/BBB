# ml_models folder
This folder is a collection of files and scripts that pertain to the development, testing, and visualization of machine learning models. 
The primary purpose of this folder is to create and test machine learning models on various inputs, which can either be numerical or categorical. 
The folder contains different types of machine learning models, such as regression models and classification models. Additionally, 
the folder contains a visualization sub-folder that contains scripts for generating different 
types of visualizations such as bar charts, logistic regression plots, confusion matrices, and others. These visualizations can be 
useful for interpreting the results of the machine learning models and for communicating those results to others. Overall, the folder 
is a valuable resource for individuals and organizations that are interested in developing and testing machine learning models on different inputs.

## Files
+ decision_tree_classification.py
+ dt_model.pkl
+ logistic_regression_model.py
+ lr_model.pkl
+ Visualization sub-folder
    + ClassificationVisualization.py
    + RegressionVisualization.py

## Using the machine learning models
Running decision_tree_classification.py will produce a decision tree model while running logistic_regression_model.py will produce a linear regression model. Both models come with these standard features/variables:
+ contains_contacts_page
+ contains_business_name
+ contains_business_name_in_copyright
+ contains_social_media_links
+ contains_reviews_page
+ contains_zipCode
+ url_contains_phone_number
+ BBBRatingScore
+ IsHQ
+ IsCharity
+ IsBBBAccredited
+ url_is_review_page

Features can be manually added or removed by going into the file of choice and finding the big list called features in decision_tree_classification.py or variables in logistic_regression_model.py, and adding/removing lines from the list. You can refer to the docstrings in the files for further modifications and documentation for help.