# Main_code_runners folder
The purpose of this folder is to contain main.py and all of the other main files. This is the primary folder where execution of our main script is ran. 

# Files
+ main_machine_learning.py
+ main_scrape_data.py
+ main_url_scrape.py
+ main.py

# Installation and Instructions
+ git clone the [repo](https://github.com/Cdahlback/BBB.git) (right click + copy link) into your local folder of choice
+ Install the following python packages:
  - Pandas            (pip install pandas)
  - BeautifulSoup     (pip install bs4)
  - sklearn           (pip install scikit-learn)
  - numpy             (pip install numpy)
  - re
  - whois
- Set necessary global variables in the following files:
  - main_machine_learning.py
  - main_scrape_data.py
  - main_url_scrape.py
- Run main.py

# SCRAPE URLs
(main_url_scrape.py)

The main_scrape_urls function takes a pandas dataframe df as an input and returns the modified dataframe with added URLs and their status codes.

## Parameters

- __df__: pandas dataframe containing business information.

## Return value

- Modified pandas dataframe with added URLs and their status codes.

## Functionality

- The function loops through each row of the input dataframe and checks if a valid URL exists in the 'Website' column.

- If it does, the function continues to the next row.

- If not, the function first tries to build a URL from the email column using the url_from_email function from create_urls.py and adds it to the 'Website' column.

- If no valid URL is found from the email column, the function then tries to find a URL from the 'BusinessName' column using the url_from_business_name function from create_urls.py and adds it to the 'Website' column.

- After adding the URLs to the 'Website' column, the function checks their status codes using the get_statuscode_forPandas function from get_status_codes.py.

- If the status code is 200, the function updates the 'Website' column with the valid URL.

- Finally, the function returns the modified dataframe.

## Functions:

- url_exists:
  - The url_exists function is a helper function for main_scrape_urls. It checks if a URL exists for the given row.

- url_from_email: 
  - The url_from_email function attempts to build a URL from the email column of a given row.

- url_from_business_name: 
  - The url_from_business_name function attempts to find a URL from the BusinessName column of a given row.


## Limitations
This script has some limitations:

- It only searches for URLs based on the business name and email.
- It only checks the status code of the URL, not the content of the website.
- It uses a fixed list of rating sites to search for URLs.

## Future Improvements
Here are some ideas for further improvements:

- Add more methods to search for URLs (e.g. by phone number or address).
- Check the content of the website to ensure it is a valid business website.
- Allow the user to specify which rating sites to search for URLs.

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

### ADDRESS EXTENSION POSSIBILITY

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
