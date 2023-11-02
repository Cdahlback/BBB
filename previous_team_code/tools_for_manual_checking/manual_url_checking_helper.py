import pandas as pd
from selenium import webdriver

df = pd.read_csv("../data/data_to_be_checked.csv", low_memory=False)  # Input file
counter = 0  # counter to keep track of how many URls have been already checked.
browser = webdriver.Chrome()  # start chromedriver.


while (
    counter < 400
):  # if counter goes above the length of how many rows will be checked, loop breaks.
    row = df.loc[counter]  # takes row at counter index.
    business_name = row["BusinessName"]  # takes business name of current row.
    address = row["StreetAddress"]  # takes street address of current row.
    city = row["City"]  # takes city of current row.
    TOB = row["TOBDescription"]  # takes type of business (TOB) for current row.
    url = row["Website"]  # takes url of current row.
    browser.get(url)  # opens chromedriver with current row's url.
    associated = input(
        "Enter 1 if associated 0 if not.\n"  # prints prompt with business name, address, and TOB.
        "Business name: {0}\n"  # also takes in input of either '0' or '1', 0 for
        "Address: {1}, {2}\n"  # if the url is not associated, 1 for if it is..
        "Type of Business: {3}\n".format(business_name, address, city, TOB)
    )
    df.loc[
        counter, "manually_checked"
    ] = associated  # sets input into a new column named "manually_checked"
    df.to_csv("data_to_be_checked.csv")  # update csv after next row has been checked
    counter += 1  # increment counter by 1
