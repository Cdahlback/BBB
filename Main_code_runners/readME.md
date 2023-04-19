Required packages to run main:
- Pandas            (pip install pandas)
- BeautifulSoup     (pip install bs4)
- sklearn           (pip install scikit-learn)
- numpy             (pip install numpy)
- re


How to run code:
- Set necessary global variables in following files
  - main_machine_learning.py
  - main_scrape_data.py
  - main_url_scrape.py
- Install required packages
- Run main.py

# SCRAPE URLs

# SCRAPE Data
(main_scrape_data.py)

This file takes a Pandas Dataframe and uses all URLs listed under each
business to scrape every possible piece of information needed. This includes
emails, and phone numbers.

### FUNCTIONS:

- scrape_data_main:
  - main function for this file. It will iterate over each row of the input Dataframe, making a call to each helper function that will scrape for the appropriate data.
  - If any of the helper functions returns any data, it will be added to the Dataframe in the correct column. If helper functions return 'None', nothing is added.
- check_email_helper:
  - Takes email, businessID, and URL of given row as variables. Extracts new emails using extract_email_data function in data_extract.py file with URL and businessID as inputs.
  - if there's no URL in the row, or an email already exists for a row, or no new emails were found, function returns 'None'.
- check_phone_helper:
  - Takes phone number, businessID, and URL of given row as variables. Extracts new emails using extract_phone_data function in data_extract.py file with URL and businessID as inputs.
  - if there's no URL in the row, or a phone number already exists for a row, or no new phone numbers were found, function returns 'None'.

### ADDRESS SCRAPER EXTENSION POSSIBILITY

There is a possibility to add an extension to this file that also scrapes for new addresses as well. As of now there is no function to scrape for address. If such function
is created in the future, the following adjustments would need to be made to this file in order to do so:
- Address helper function would need to be coded that calls the address scraper function.
- Main function would also need to add any newly found address into the 'StreetAddress' column of the Dataframe.


# MACHINE LEARNING - ML 
(main_machine_learning.py)


## DECISION TREE:

In the global variables section located near the top of the file you will fill out values for the ML model as well as features you plan to include for the model.

### Suggestions for model inputs: 
(docs: https://scikit-learn.org/stable/modules/tree.html)
- max_depth: The model yields the highest results when this is at 4. We experimented with values from 3-7.
- ccp_value: We had intents of using this value to lower the type II errors (false positives - FP), however, it seemed to have no impact and even raise the FP with some inputs.

### FUNCTIONS:

- main_ml: 
  - Function which performs all actions of this file, it takes in two dataframes as well as a stream of data. We iterate over our updated dataframe and see if we found any new information for it. If new information is found for a row, we add it to the stream of data.
  - We organized our final output to be this stream of data. It should take the following form. (implement graph)
- add_to_stream
  - Used as a helper function of main_ml by collecting all new data found and placing it in a stream of data.
  - utilized three helper functions _new_data_found(), which determine if new data has been found for that rows specific data type.
- can_predict
  - We cannot predict rows with no url, this function is called by main_ml and covers that functionallity.

### VISUALIZATIONS/STATS
We provide the following visuals for a DecisionTreeClassification Model:
- Confusion Matrix
  - Used for displaying TP (true positive), TN, FP, FN (false negative)
  - Helpful for determining how many FP the model is outputting, as requested by the BBB. 
  - Also displays things like accuracy, precision, f1-score, micro-avg, etc. All used to measure a classification models performance. 
  - scikit learn docs here: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
  - useful resources for interpret results: https://www.v7labs.com/blog/confusion-matrix-guide
- ROC Curve
  - A ROC (Receiver Operating Characteristic) curve is a graphical representation of the performance of a classification model at different classification thresholds.
  - In a ROC curve, the x-axis represents the false positive rate (FPR), and the y-axis represents the true positive rate (TPR).
  - AUC: area under curve
  - A perfect classifier would have an AUC of 1, indicating that it achieves a TPR of 1 and an FPR of 0. A random classifier would have an AUC of 0.5, indicating that it performs no better than chance.
  - scikit learn docs: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html
  - helpful for interpretation: https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5
