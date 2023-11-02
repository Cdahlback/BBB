import pandas as pd
from selenium import webdriver

df = pd.read_csv("../data/manually_verify_scrapers.csv")
manually_verify = df.sample(50)  # input csv with sample data to test.
browser = webdriver.Chrome()  # open chromedriver.


def print_info(row):
    """
    helper function that prints all the information from the independent variables we want to manually check.
    :param row: row in sample dataframe
    """
    print("BusinessName: {0}".format(row["BusinessName"]))
    print("url_contains_email: {0}".format(row["url_contains_phone_number"]))
    print("contains_contacts_page: {0}".format(row["contains_contacts_page"]))
    print("contains_business_name: {0}".format(row["contains_business_name"]))
    print(
        "contains_business_name_in_copyright: {0}".format(
            row["contains_business_name_in_copyright"]
        )
    )
    print("contains_social_media_links: {0}".format(row["contains_social_media_links"]))
    print("contains_reviews_page: {0}".format(row["contains_reviews_page"]))
    print("contains_zipCode: {0}".format(row["contains_zipCode"]))
    print("contains_phone_number: {0}".format(row["url_contains_phone_number"]))
    print("")


for index, row in manually_verify.iterrows():  # iterate over all manually_verify rows.
    try:
        browser.get(row["Website"])  # try loading the url into the chromedriver.
    except:
        print(
            "Website failed to load"
        )  # if url doesn't exist, except error and print statement.
    finally:
        print_info(row)  # print row information to use for manually verifying.
        ipt = input(
            "Press any key to continue"
        )  # takes in any input to move on to next url.
