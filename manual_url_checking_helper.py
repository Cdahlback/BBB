from selenium import webdriver
import pandas as pd
import random
import numpy as np

"""MUST CLEAN ALL URLS PRIOR TO RUNNING THIS SCRIPT"""

df = pd.read_csv('data/mn_bbb_businesses.csv', low_memory=False)
counter = 0
browser = webdriver.Chrome()
# set containing all urls we've gone through
s = set()

while counter < 400:
    df["checked_manually"] = np.nan
    row_index = random.randint(0, len(df) - 1)
    row = df.loc[row_index]
    row_idx = row["BusinessID"]
    business_name = row["BusinessName"]
    url = row["Website"]
    if url in s or url is np.nan:
        continue
    else:
        s.add(url)
        browser.get(url)
        associated = input("Enter 1 if associated with {0}, 0 if not".format(business_name))
        df.loc[row_idx, "manually_checked"] = associated


# Psudo
# add a new column to the datafram (checked_manually), set all to nan
# Randomly pick a row from the dataframe
# check if we have got this row before, continue if so
# Extract the name and website for that row
# Open the url with selenium
# wait for a user input (0 or 1)
# update the column checked_manually with the result (0 or 1)

