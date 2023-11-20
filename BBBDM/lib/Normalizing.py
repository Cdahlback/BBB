import re
import logging
import pandas as pd
from i18naddress import normalize_address
from email_validator import validate_email, EmailNotValidError
# Setup logging to capture detailed logs about warnings, errors, and other critical information.
logging.basicConfig(filename='functions.log', level=logging.DEBUG)

def normalize_email(email:str) ->str:
    """
This is a helper function that normalizes the email to fit BBB expectations

:param email: str of the emial

:returns: email as a str that is normalized"""

    try:
        # Normalize and validate the email using email-validator library
        # 1. Strip leading and trailing spaces in the email
        # 2. Convert all characters to lowercase
        # 3. Remove non-alphanumeric characters except for . _ - @
        normalized_email = ''.join(e.lower() for e in email.strip() if e.isalnum() or e in '._-@')
        #normalized the valid email
        valid_email = validate_email(normalized_email).normalized
        logging.info("Valid email normalized")
        return valid_email
    except EmailNotValidError as e:
     # Handle invalid emails by logging and returning the original email
        logging.debug(f'Invalid email: {str(e)}')
        return email  # Return the original email for invalid ones
    
def normalize_zipcode(zipcode_list):
    standardized_zipcodes = []

    for zipcode in zipcode_list:
        try:
            # Remove white spaces and non-numeric characters
            standardized_zipcode = re.sub(r'\s|\D', '', zipcode)

            # Check if the standardized zipcode has a length of 5
            if len(standardized_zipcode) == 5:
                standardized_zipcodes.append(standardized_zipcode)
            else:
                standardized_zipcodes.append("N/A")
        except Exception as e:
            # Handle exceptions by marking the zip code as "Error"
            logging.debug(f"Error processing zip code '{zipcode}': {str(e)}")
            standardized_zipcodes.append("Error")

    # Create a DataFrame
    data = {'Original Zip Code': zipcode_list, 'Standardized Zip Code': standardized_zipcodes}
    df = pd.DataFrame(data)

    return df
    
    return normalized_zipcodes
def normalize_dataframe(df:pd.DataFrame) -> pd.DataFrame:
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
    digits = ''.join(filter(str.isdigit, phone_str))
    if len(digits) == 10:
        return f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        raise ValueError(f"'{phone_str}' does not match valid U.S. phone number formats.")

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
    name = re.sub('&', ' and ', name)
    name = re.sub('[^a-z\s-]', '', name)
    name = re.sub(' {2,}', ' ', name)
    return name.strip()

def normalize_address_i18n(raw_address: str) -> str:
    """
    Utilizes the i18naddress library to normalize and structure address data.
    
    Parameters:
    - raw_address (dict): Dictionary containing raw address details.
    
    Returns:
    - dict: A structured and normalized address dictionary.
    """
    try:
        address_list = raw_address.split(',')
        address_dict = {
            'street_address': address_list[0],
            'city': address_list[1].split(' ')[0],
            'country_area': 'MN',
            'postal_code': address_list[1].split(' ')[1]
        }
        normalized_address = normalize_address(address_dict)
        logging.info(f"Successfully normalized address: {normalized_address}")
        normalize_address = f"{normalized_address['street_address']},{normalized_address['city']} {normalized_address['postal_code']}"
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
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    logging.info(f"Successfully normalized URL: {url}")
    return url

if __name__ == "__main__":
    # Execute a series of tests to verify the functionality of the normalization functions.
    business_name = "Example & Co."
    print("Normalized Business Name:", standardizeName(business_name))
    
    raw_address = {
        'country_area': 'CA',
        'locality': 'Mountain View',
        'postal_code': '94041',
        'street_address': '1600 Amphitheatre Pkwy'
    }
    print("Normalized Address:", normalize_address_i18n(raw_address))
    
    url = "www.Example.com"
    print("Normalized URL:", normalize_url(url))