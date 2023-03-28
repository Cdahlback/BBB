from selenium import webdriver
import pandas as pd

"""MUST CLEAN ALL URLS PRIOR TO RUNNING THIS SCRIPT"""

df = pd.read_csv('../data/data_to_be_checked.csv', low_memory=False)
counter = 0
browser = webdriver.Chrome()



while counter < 400:
    row = df.loc[counter]
    business_name = row["BusinessName"]
    address = row['StreetAddress']
    city = row['City']
    TOB = row['TOBDescription']
    url = row["Website"]
    browser.get(url)
    associated = input("Enter 1 if associated 0 if not.\n"
                       "Business name: {0}\n"
                       "Address: {1}, {2}\n"
                       "Type of Business: {3}\n".format(business_name, address, city, TOB))
    df.loc[counter, "manually_checked"] = associated
    df.to_csv('data_to_be_checked.csv')
    counter += 1


# Psudo
# add a new column to the datafram (checked_manually), set all to nan
# Randomly pick a row from the dataframe
# check if we have got this row before, continue if so
# Extract the name and website for that row
# Open the url with selenium
# wait for a user input (0 or 1)
# update the column checked_manually with the result (0 or 1)