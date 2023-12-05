import logging
import re

import pandas as pd
from email_validator import EmailNotValidError, validate_email
from i18naddress import normalize_address
from pandarallel import pandarallel

# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename="functions.log", level=logging.DEBUG)

pandarallel.initialize()

def normalize_email(emails):
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
            normalized_emails.append(email)
            continue
        try:
            # Steps 1-3
            normalized_email = "".join(
                e.lower() for e in email.strip() if e.isalnum() or e in "._-@"
            )
            # Step 4
            valid_email = validate_email(normalized_email).normalized
            logging.info("Valid email normalized")
            normalized_emails.append(valid_email)
        except EmailNotValidError as e:
            logging.debug(f"{email} not valid, removing from email list")
            continue

    return normalized_emails


def normalize_zipcode(zipcodes):
    """
    Function to normalize a list of zipcodes for a business

    :param zipcodes: list of zipcode values for a SPECIFIC business
    1. Removed non-numeric characters
    2. Ensures length of 5
    """
    normalized_zipcodes = []

    for zipcode in zipcodes:
        if not isinstance(zipcode, str):
            normalized_zipcodes.append(zipcode)
            continue
        try:
            # Remove white spaces and non-numeric characters
            standardized_zipcode = re.sub(r"\s|\D", "", zipcode)

            # Check if the standardized zipcode has a length of 5
            if len(standardized_zipcode) == 5:
                normalized_zipcodes.append(standardized_zipcode)
        except Exception as e:
            logging.debug(f"{zipcode} not valid, removing from zipcode list")
            continue

    return normalized_zipcodes


def normalize_dataframe(df):
    """
    This function serves to normalize various columns within a given DataFrame. The columns targeted for normalization
    include "Email", "Phone Number", and "Zipcode". Each of these columns are subjected to their designated normalization
    functions. Any invalid entries detected during this process are substituted with None.

    Parameters:
    - df (pd.DataFrame): The original DataFrame that needs normalization.

    Returns:
    - pd.DataFrame: Returns the DataFrame after normalization.
    """
    df["Email"] = df["Email"].parallel_apply(normalize_email)
    df["Phone"] = df["Phone"].parallel_apply(normalize_us_phone_number)
    df["Zipcode"] = df["Zipcode"].parallel_apply(normalize_zipcode)
    df["BusinessName"] = df["BusinessName"].parallel_apply(standardizeName)
    df["Website"] = df["Website"].parallel_apply(normalize_url)
    df["Address"] = df["Address"].parallel_apply(normalize_address_i18n)
    return df


def normalize_us_phone_number(phones):
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
    if not isinstance(phones, list):
        digits = "".join(filter(str.isdigit, phones))
        if len(digits) == 10:
            normalized_phones = f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == "1":
            normalized_phones = f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
        else:
            logging.info(f"{phones} not valid, removing from phone list")
            return ""
        return normalized_phones
    for phone in phones:
        if not isinstance(phone, str):
            normalized_phones.append(phone)
            continue
        digits = "".join(filter(str.isdigit, phone))
        if len(digits) == 10:
            normalized_phones.append(f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}")
        elif len(digits) == 11 and digits[0] == "1":
            normalized_phones.append(
                f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
            )
        else:
            logging.info(f"{phone} not valid, removing from phone list")
            continue

    return normalized_phones


def standardizeName(names, is_sos=False):
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
    if not isinstance(names, list):
        try:
            names = names.lower()
            names = re.sub("&", " and ", names)
            names = re.sub(r"[^a-z\s-]", "", names)
            names = re.sub(r" {2,}", " ", names)
            normalized_names = names
        except Exception as e:
            logging.info(f"{names} not valid, removing from list")
            return ""
        return normalized_names
    for name in names:
        if not isinstance(name, str):
            normalized_names.append(name)
            continue
        try:
            name = name.lower()
            name = re.sub("&", " and ", name)
            name = re.sub(r"[^a-z\s-]", "", name)
            name = re.sub(r" {2,}", " ", name)
            normalized_names.append(name)
        except Exception as e:
            logging.info(f"{name} not valid, removing from list")
            continue

    if is_sos:
        normalized_names = [
            name.replace("llc", "") if isinstance(name, str) else name
            for name in normalized_names
        ]
        normalized_names = [
            name.replace("l l c", "") if isinstance(name, str) else name
            for name in normalized_names
        ]
        normalized_names = [
            name.replace("inc", "") if isinstance(name, str) else name
            for name in normalized_names
        ]
        normalized_names = [
            name.replace("co", "") if isinstance(name, str) else name
            for name in normalized_names
        ]
        normalized_names = [
            name.replace("ltd", "") if isinstance(name, str) else name
            for name in normalized_names
        ]
        normalized_names = [
            name.rstrip() if isinstance(name, str) else name
            for name in normalized_names
        ]

    return normalized_names


def normalize_name(name):
    """
    Replaces llc, l l c, inc, co, ltd with empty
    """
    name = name.replace("llc", "") if isinstance(name, str) else name
    name = name.rstrip() if isinstance(name, str) else name
    return name


def normalize_address_i18n(addresses):
    """
    Utilizes the i18naddress library to normalize and structure address data.

    Parameters:
    - raw_address (list[str]): Contains list of raw address details.

    Returns:
    - list[str]: A structured and normalized address list.
    """
    normalized_addresses = []
    if not isinstance(addresses, list):
        try:
            address_list = addresses.split(",")
            address_dict = {
                "street_address": address_list[0],
                "city": address_list[1],
                "country_area": "Minnesota",
                "country_code": "US",
                "postal_code": address_list[2],
            }
            normalized_address = normalize_address(address_dict)
            logging.info(f"Successfully normalized address: {normalized_address}")
            valid_normalize_address = f"{normalized_address['street_address']},{normalized_address['city'].lower()},{normalized_address['postal_code']}"
            normalized_addresses = valid_normalize_address
        except Exception as e:
            logging.error(f"{addresses} not valid, removing from address list")
            return addresses
        return normalized_addresses
    for address in addresses:
        if not isinstance(address, str):
            normalized_addresses.append(address)
            continue
        try:
            address_list = address.split(",")
            address_dict = {
                "street_address": address_list[0],
                "city": address_list[1],
                "country_area": "Minnesota",
                "country_code": "US",
                "postal_code": address_list[2],
            }
            normalized_address = normalize_address(address_dict)
            logging.info(f"Successfully normalized address: {normalized_address}")
            valid_normalize_address = f"{normalized_address['street_address']},{normalized_address['city'].lower()},{normalized_address['postal_code']}"
            normalized_addresses.append(valid_normalize_address)
        except Exception as e:
            logging.error(f"{address} not valid, removing from address list")
            continue

    return normalized_addresses


def normalize_url(urls):
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
    if not isinstance(urls, list):
        try:
            url = urls.lower().replace(" ", "")
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            logging.info(f"Successfully normalized URL: {url}")
            normalized_urls = url
        except Exception as e:
            logging.info(f"{urls} not valid, removing from list")
            return ""
        return normalized_urls
    for url in urls:
        if not isinstance(url, str):
            normalized_urls.append(url)
            continue
        try:
            url = url.lower().replace(" ", "")
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            logging.info(f"Successfully normalized URL: {url}")
            normalized_urls.append(url)
        except Exception as e:
            logging.info(f"{url} not valid, removing from list")

    return normalized_urls


if __name__ == "__main__":
    # Execute a series of tests to verify the functionality of the normalization functions.
    # business_name = ["Example & Co."]
    # print("Normalized Business Name:", standardizeName(business_name))

    raw_address = ["2200 Nicollet Ave, Minneapolis, 55404"]
    print("Normalized Address:", normalize_address_i18n(raw_address))

    # url = ["www.Example.com"]
    # print("Normalized URL:", normalize_url(url))
    #
    # phone = ["6512224355"]
    # print("Normalized Phone: ", normalize_us_phone_number(phone))
    #
    # email = ["jimalbinson@gmail.com"]
    # print("Normalized Email: ", normalize_email(email))
