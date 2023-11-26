import re
import logging
import pandas as pd
from i18naddress import normalize_address
from email_validator import validate_email, EmailNotValidError
# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


def normalize_email(emails: list[str]) -> list[str]:
    """
    This is a helper function that normalizes the email to fit BBB expectations
    1. Strip spaces
    2. Convert to lowercase
    3. Remove non-alphanumeric except for . _ - @
    4. Validate the email with our validate_email package function

    :param emails: list of email values for a SPECIFIC business

    :returns: email as a str that is normalized"""
    normalized_emails = []

    for email in emails:
        if not isinstance(email, str):
            continue
        try:
            # Steps 1-3
            normalized_email = ''.join(e.lower() for e in email.strip() if e.isalnum() or e in '._-@')
            # Step 4
            valid_email = validate_email(normalized_email).normalized
            logging.info("Valid email normalized")
            normalized_emails.append(valid_email)
        except EmailNotValidError as e:
            logging.debug(f'{email} not valid, removing from email list')
            continue

    return normalized_emails

    
def normalize_zipcode(zipcodes: list[str]) -> list[str]:
    """
    Function to normalize a list of zipcodes for a business

    :param zipcodes: list of zipcode values for a SPECIFIC business
    1. Removed non-numeric characters
    2. Ensures length of 5
    """
    normalized_zipcodes = []

    for zipcode in zipcodes:
        if not isinstance(zipcode, str):
            continue
        try:
            # Remove white spaces and non-numeric characters
            standardized_zipcode = re.sub(r'\s|\D', '', zipcode)

            # Check if the standardized zipcode has a length of 5
            if len(standardized_zipcode) == 5:
                normalized_zipcodes.append(standardized_zipcode)
        except Exception as e:
            logging.debug(f"{zipcode} not valid, removing from zipcode list")
            continue
  
    return normalized_zipcodes
    

def normalize_dataframe(df: list[str]) -> list[str]:
    """
    This function serves to normalize various columns within a given DataFrame. The columns targeted for normalization
    include "Email", "Phone Number", and "Zipcode". Each of these columns are subjected to their designated normalization 
    functions. Any invalid entries detected during this process are substituted with None.
    
    Parameters:
    - df (pd.DataFrame): The original DataFrame that needs normalization.
    
    Returns:
    - pd.DataFrame: Returns the DataFrame after normalization.
    """
    df['Email'] = df['Email'].apply(normalize_email)
    df['Phone Number'] = df['Phone Number'].apply(normalize_us_phone_number)
    df['Zipcode'] = df['Zipcode'].apply(normalize_zipcode)
    df['BusinessName'] = df['BusinessName'].apply(standardizeName)
    df['Website'] = df['Website'].apply(normalize_url)
    df['Address'] = df['Address'].apply(normalize_address_i18n)
    return df


def normalize_us_phone_number(phones: list[str]) -> list[str]:
    """
    Designed to process U.S. phone numbers, this function:
    1. Extracts all numeric digits.
    2. Formats the digits according to the standard U.S. phone number format.
    
    If the input doesn't match expected lengths for U.S. phone numbers, a ValueError is raised.
    
    Parameters:
    - phone_str (str): The list of raw phone number strings to be normalized.
    
    Returns:
    - list[str]: Returns the normalized U.S. phone number.
    """
    normalized_phones = []
    for phone in phones:
        if not isinstance(phone, str):
            continue
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            normalized_phones.append(f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}")
        elif len(digits) == 11 and digits[0] == '1':
            normalized_phones.append(f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}")
        else:
            logging.info(f"{phone} not valid, removing from phone list")
            continue

    return normalized_phones


def standardizeName(names: list[str]) -> list[str]:
    """
    This function standardizes business names by:
    1. Converting the entire name to lowercase.
    2. Substituting '&' with ' and '.
    3. Removing characters not found in the set [a-z, whitespace, -].
    4. Trimming extra spaces.
    
    Parameters:
    - name (list[str]): The business names that requires standardization.
    
    Returns:
    - str: Returns a list of the standardized business names.
    """
    normalized_names = []
    for name in names:
        if not isinstance(name, str):
            continue
        try:
            name = name.lower()
            name = re.sub('&', ' and ', name)
            name = re.sub(r'[^a-z\s-]', '', name)
            name = re.sub(r' {2,}', ' ', name)
            normalized_names.append(name)
        except Exception as e:
            logging.info(f"{name} not valid, removing from list")
            continue
    return normalized_names


def normalize_address_i18n(addresses: list[str]) -> list[str]:
    """
    Utilizes the i18naddress library to normalize and structure address data.
    
    Parameters:
    - raw_address (list[str]): Contains list of raw address details.
    
    Returns:
    - list[str]: A structured and normalized address list.
    """
    normalized_addresses = []
    for address in addresses:
        try:
            address_list = address.split(',')
            address_dict = {
                'street_address': address_list[0],
                'city': address_list[1],
                'country_area': 'Minnesota',
                'country_code': 'US',
                'postal_code': address_list[2]
            }
            normalized_address = normalize_address(address_dict)
            logging.info(f"Successfully normalized address: {normalized_address}")
            valid_normalize_address = f"{normalized_address['street_address']},{normalized_address['city'].lower()},{normalized_address['postal_code']}"
            normalized_addresses.append(valid_normalize_address)
        except Exception as e:
            logging.error(f"{address} not valid, removing from address list")
            continue

    return normalized_addresses


def normalize_url(urls: list[str]) -> list[str]:
    """
    This function normalizes URLs by:
    1. Converting the entire URL to lowercase.
    2. Eliminating spaces.
    3. Appending 'http://' at the beginning if no protocol (http or https) is present.
    
    Parameters:
    - url (str): The URL that needs to be normalized.
    
    Returns:
    - str: Returns the normalized URL.
    """
    normalized_urls = []
    for url in urls:
        try:
            url = url.lower().replace(" ", "")
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            logging.info(f"Successfully normalized URL: {url}")
            normalized_urls.append(url)
        except Exception as e:
            logging.info(f"{url} not valid, removing from list")

    return normalized_urls


if __name__ == "__main__":
    # Execute a series of tests to verify the functionality of the normalization functions.
    business_name = ["Example & Co."]
    print("Normalized Business Name:", standardizeName(business_name))
    
    raw_address = ["78 Acker St E, Saint Paul, 55117"]
    print("Normalized Address:", normalize_address_i18n(raw_address))
    
    url = ["www.Example.com"]
    print("Normalized URL:", normalize_url(url))

    phone = ["6512224355"]
    print("Normalized Phone: ", normalize_us_phone_number(phone))

    email = ["jimalbinson@gmail.com"]
    print("Normalized Email: ", normalize_email(email))