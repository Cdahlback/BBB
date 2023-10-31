import re
import logging
import pandas as pd
from i18naddress import normalize_address


# Configure logging to capture warnings, errors, and other important information.
logging.basicConfig(filename='functions.log', level=logging.DEBUG)

def normalize_email(email:str) -> str:
    """
    Normalize email addresses by:
    - Converting to lowercase
    - Removing whitespace
    - Removing special characters (except ., @, and -)
    If the email address lacks an @ symbol, it is considered invalid and None is returned.
    
    Parameters:
    - email (str): Email address to normalize.
    
    Returns:
    - str | None: Normalized email address or None if invalid.
    """
    email = email.lower()  
    email = re.sub(r'\s', '', email)  
    email = re.sub(r'[^a-z0-9.@-]', '', email)
    if '@' not in email:
        logging.warning(f'Invalid email: {email}')
        return None  
    return email

def normalize_zipcode(zipcode:str) -> str:
    """
    Normalize zipcodes by:
    - Removing whitespace
    - Removing non-numeric characters
    Zipcodes should contain exactly 5 numeric digits. If not, they are considered invalid.
    
    Parameters:
    - zipcode (str): Zipcode to normalize.
    
    Returns:
    - str | None: Normalized zipcode or None if invalid.
    """
    zipcode = re.sub(r'\s|\D', '', zipcode)  
    if len(zipcode) == 5:
        return zipcode
    else:
        logging.warning(f'Invalid zipcode: {zipcode}')
        return None

def normalize_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame columns using appropriate functions. 
    The Email, Phone Number, and Zipcode columns are processed by their respective normalization functions.
    Invalid entries are replaced with None.
    
    Parameters:
    - df (pd.DataFrame): DataFrame to normalize.
    
    Returns:
    - pd.DataFrame: Normalized DataFrame.
    """
    df['Email'] = df['Email'].apply(normalize_email)
    df['Phone Number'] = df['Phone Number'].apply(normalize_us_phone_number)
    df['Zipcode'] = df['Zipcode'].apply(normalize_zipcode)
    return df

def normalize_us_phone_number(phone_str: str) -> str:
    """
    Normalize U.S. phone numbers to a standard format by:
    - Removing non-digit characters
    - Formatting to standard U.S. phone number format
    
    Parameters:
    - phone_str (str): Phone number string to normalize.
    
    Returns:
    - str: Normalized U.S. phone number.
    """
    digits = ''.join(filter(str.isdigit, phone_str))
    if len(digits) == 10:
        return f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        raise ValueError(f"'{phone_str}' is not a valid U.S. phone number.")

def standardizeName(name: str) -> str:
    """
    Standardize business names by:
    - Converting to lowercase
    - Replacing '&' with ' and '
    - Removing characters not in the set [a-z, whitespace, -]
    - Removing extra spaces
    
    Parameters:
    - name (str): Business name to standardize.
    
    Returns:
    - str: Standardized business name.
    """
    name = name.lower()
    name = re.sub('&', ' and ', name)
    name = re.sub('[^a-z\s-]', '', name)
    name = re.sub(' {2,}', ' ', name)
    return name.strip()

def normalize_address_i18n(raw_address: dict) -> dict:
    """
    Normalize and structure address data using the i18naddress library.
    
    Parameters:
    - raw_address (dict): Raw address details in dictionary format.
    
    Returns:
    - dict: Normalized address details.
    """
    try:
        normalized_address = normalize_address(raw_address)
        logging.info(f"Normalized Address: {normalized_address}")
        return normalized_address
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None

def normalize_url(url: str) -> str:
    """
    Normalize URLs by:
    - Converting to lowercase
    - Removing spaces
    - Prefixing with 'http://' if protocol is absent
    
    Parameters:
    - url (str): URL to normalize.
    
    Returns:
    - str: Normalized URL.
    """
    url = url.lower().replace(" ", "")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    logging.info(f"Normalized URL: {url}")
    return url

if __name__ == "__main__":
    # Test the normalization functions.
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
