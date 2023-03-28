from selenium import webdriver
import pandas as pd
import random
import numpy as np

"""
MUST CLEAN ALL URLS PRIOR TO RUNNING THIS SCRIPT
Used to help assist our team in automating the manual checking process
Uses selenium to open webpages
"""

df = pd.read_csv('data/mn_bbb_businesses.csv', low_memory=False)
counter = 0
browser = webdriver.Chrome()

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


