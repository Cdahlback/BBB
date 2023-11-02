import logging
import re

import pandas as pd
from i18naddress import normalize_address

# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename="functions.log", level=logging.DEBUG)


def normalize_email(email: str) -> str:
    """
    This function is designed to handle the normalization of email addresses. It carries out the following steps:
    1. Converts the email address to lowercase.
    2. Removes any whitespace.
    3. Filters out any special characters with the exception of ".", "@", and "-".

    Should the processed email lack an "@" symbol, it will be deemed as invalid and will return None.

    Parameters:
    - email (str): The raw email address that needs to be normalized.

    Returns:
    - str | None: Returns the normalized email if valid, otherwise None.
    """
    email = email.lower()
    email = re.sub(r"\s", "", email)
    email = re.sub(r"[^a-z0-9.@-]", "", email)
    if "@" not in email:
        logging.warning(f"Encountered an invalid email format: {email}")
        return None
    return email


def normalize_zipcode(zipcode: str) -> str:
    """
    This function processes and validates zip codes. Specifically, it:
    1. Removes any whitespace.
    2. Filters out any non-numeric characters.

    If the resultant zipcode does not comprise exactly 5 numeric digits, it's deemed as invalid.

    Parameters:
    - zipcode (str): The raw zipcode that needs to be normalized.

    Returns:
    - str | None: Returns the processed zipcode if valid, otherwise None.
    """
    zipcode = re.sub(r"\s|\D", "", zipcode)
    if len(zipcode) != 5:
        logging.warning(f"Detected an invalid zipcode format: {zipcode}")
        return None
    return zipcode


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function serves to normalize various columns within a given DataFrame. The columns targeted for normalization
    include "Email", "Phone Number", and "Zipcode". Each of these columns are subjected to their designated normalization
    functions. Any invalid entries detected during this process are substituted with None.

    Parameters:
    - df (pd.DataFrame): The original DataFrame that needs normalization.

    Returns:
    - pd.DataFrame: Returns the DataFrame after normalization.
    """
    df["Email"] = df["Email"].apply(normalize_email)
    df["Phone Number"] = df["Phone Number"].apply(normalize_us_phone_number)
    df["Zipcode"] = df["Zipcode"].apply(normalize_zipcode)
    df["BusinessName"] = df["BusinessName"].apply(standardizeName)
    df["Website"] = df["Website"].apply(normalize_url)
    df["Address"] = df["Address"].apply(normalize_address_i18n)
    return df


def normalize_us_phone_number(phone_str: str) -> str:
    """
    Designed to process U.S. phone numbers, this function:
    1. Extracts all numeric digits.
    2. Formats the digits according to the standard U.S. phone number format.

    If the input doesn't match expected lengths for U.S. phone numbers, a ValueError is raised.

    Parameters:
    - phone_str (str): The raw phone number string to be normalized.

    Returns:
    - str: Returns the normalized U.S. phone number.
    """
    digits = "".join(filter(str.isdigit, phone_str))
    if len(digits) == 10:
        return f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == "1":
        return f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        raise ValueError(
            f"'{phone_str}' does not match valid U.S. phone number formats."
        )


def standardizeName(name: str) -> str:
    """
    This function standardizes business names by:
    1. Converting the entire name to lowercase.
    2. Substituting '&' with ' and '.
    3. Removing characters not found in the set [a-z, whitespace, -].
    4. Trimming extra spaces.

    Parameters:
    - name (str): The business name that requires standardization.

    Returns:
    - str: Returns the standardized business name.
    """
    name = name.lower()
    name = re.sub("&", " and ", name)
    name = re.sub("[^a-z\s-]", "", name)
    name = re.sub(" {2,}", " ", name)
    return name.strip()


def normalize_address_i18n(raw_address: dict) -> dict:
    """
    Utilizes the i18naddress library to normalize and structure address data.

    Parameters:
    - raw_address (dict): Dictionary containing raw address details.

    Returns:
    - dict: A structured and normalized address dictionary.
    """
    try:
        normalized_address = normalize_address(raw_address)
        logging.info(f"Successfully normalized address: {normalized_address}")
        return normalized_address
    except Exception as e:
        logging.error(f"Failed to normalize address due to error: {str(e)}")
        return None


def normalize_url(url: str) -> str:
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
    url = url.lower().replace(" ", "")
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    logging.info(f"Successfully normalized URL: {url}")
    return url


if __name__ == "__main__":
    # Execute a series of tests to verify the functionality of the normalization functions.
    business_name = "Example & Co."
    print("Normalized Business Name:", standardizeName(business_name))

    raw_address = {
        "country_area": "CA",
        "locality": "Mountain View",
        "postal_code": "94041",
        "street_address": "1600 Amphitheatre Pkwy",
    }
    print("Normalized Address:", normalize_address_i18n(raw_address))

    url = "www.Example.com"
    print("Normalized URL:", normalize_url(url))
