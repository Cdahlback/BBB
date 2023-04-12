from Extract_Data.data_extraction import extract_email_data, extract_phone_data
import pandas as pd


def scrape_data_main(df):
    """
    :param df: dataframe that will be searched for data
    :return: updated dataframe with updated data
    """
    for index, row in df.iterrows():                    # iterate through rows
        new_emails = check_email_helper(row)            # run email checker on rows
        if new_emails is not None:
            df.at[index, 'Email'] = new_emails          # if checker came back not None, set new emails
        new_phones = check_phone_number_helper(row)     # run phone checker on rows
        if new_phones is not None:
            df.at[index, 'Phone'] = new_phones          # if checker came back non None, set new phone numbers
        # Can do the same for addresses later on when function is created


def check_email_helper(row):
    """
    :param row: indexed row from dataframe
    :return: dictionary of possible emails if needed, otherwise None
    """
    email = row['Email']                # grab email from row
    business_id = row['BusinessID']     # grab business ID from row
    url = row['Website']                # grab website from row
    if pd.isnull(url):                  # if url doesn't exist, return None because we can't run anything without it
        return None
    if pd.isnull(email):                # if email is missing, extract list of emails, and return dict
        dict_email = extract_email_data(business_id, url)
        return dict_email
    else:
        return None                     # if email already exists, return None


def check_phone_number_helper(row):
    """
    :param row: indexed row from dataframe
    :return: dictionary of all possible phone numbers if needed, otherwise none
    """
    phone = row['Phone']                 # grab phone number from row
    business_id = row['BusinessID']      # grab business ID from row
    url = row['Website']                 # grab website from row
    if pd.isnull(url):                   # if url doesn't exist, return None because we can't run anything without it
        return None
    if pd.isnull(phone):                 # if phone is missing, extract list of phones, and return dict
        dict_phone = extract_phone_data(business_id, url)
        return dict_phone
    else:
        return None                      # if phone already exists, return None


if __name__ == '__main__':
    input_df = pd.read_csv('input_csv')
    scrape_data_main(input_df)
