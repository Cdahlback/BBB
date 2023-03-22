from selenium import webdriver
import pandas as pd
import random
import numpy as np

"""MUST CLEAN ALL URLS PRIOR TO RUNNING THIS SCRIPT"""

df = pd.read_csv('data/dylan_manual_check.csv', low_memory=False)
counter = 0
browser = webdriver.Chrome()

# set containing all urls we've gone through, must update after each person has done a portion of
# their 400
s = set()

while counter < 400:
    row_index = random.randint(1, len(df) - 1)
    row = df.loc[row_index]
    business_name = row["BusinessName"]
    url = row["Website"]
    if url in s or url is np.nan:
        continue
    else:
        counter += 1
        s.add(url)
        browser.get(url)
        associated = input("Enter 1 if associated with {0}, 0 if not".format(business_name))
        df.loc[row_index, "manually_checked"] = associated


# Psudo
# add a new column to the datafram (checked_manually), set all to nan
# Randomly pick a row from the dataframe
# check if we have got this row before, continue if so
# Extract the name and website for that row
# Open the url with selenium
# wait for a user input (0 or 1)
# update the column checked_manually with the result (0 or 1)

