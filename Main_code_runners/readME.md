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

# SCRAPE DATA

# SCRAPE URLs


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
