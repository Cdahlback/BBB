import pandas as pd
from selenium import webdriver

df = pd.read_csv("../data/manually_verify_scrapers.csv")
manually_verify = df.sample(50)
browser = webdriver.Chrome()


def print_info(row):
    print("BusinessName: {0}".format(row['BusinessName']))
    print("url_contains_email: {0}".format(row["url_contains_phone_number"]))
    print("contains_contacts_page: {0}".format(row["contains_contacts_page"]))
    print("contains_business_name: {0}".format(row["contains_business_name"]))
    print("contains_business_name_in_copyright: {0}".format(row["contains_business_name_in_copyright"]))
    print("contains_social_media_links: {0}".format(row["contains_social_media_links"]))
    print("contains_reviews_page: {0}".format(row["contains_reviews_page"]))
    print("contains_zipCode: {0}".format(row["contains_zipCode"]))
    print("contains_phone_number: {0}".format(row["url_contains_phone_number"]))
    print("")


for index, row in manually_verify.iterrows():
    try:
        browser.get(row['Website'])
    except:
        print("Website failed to load")
    finally:
        print_info(row)
        ipt = input("Press any key to continue")

