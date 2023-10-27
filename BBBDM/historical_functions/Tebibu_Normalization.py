import re
import logging
from i18naddress import normalize_address

# Logging setup
logging.basicConfig(filename='normalization.log', level=logging.INFO)

def normalize_us_phone_number(phone_str: str) -> str:
    """
    Normalizes U.S. phone numbers to a standard format.
    """
    # Remove non-digit characters
    digits = ''.join(filter(str.isdigit, phone_str))
    
    if len(digits) == 10:
        return f"+1 {digits[:3]}-{digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+{digits[0]} {digits[1:4]}-{digits[4:7]}-{digits[7:]}"
    else:
        raise ValueError(f"'{phone_str}' is not a valid U.S. phone number.")

def standardizeName(name: str) -> str:
    """
    Standardizes business names by making various modifications.
    """
    name = name.lower()
    name = re.sub('&', ' and ', name)
    name = re.sub('[^a-z\s-]', '', name)
    name = re.sub(' {2,}', ' ', name)
    return name.strip()

def normalize_address_i18n(raw_address: dict) -> dict:
    """
    Normalizes address using the i18naddress library.
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
    Normalizes URLs by adding "http://" if not present.
    """
    url = url.lower().replace(" ", "")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    logging.info(f"Normalized URL: {url}")
    return url

if __name__ == "__main__":
    # Testing the normalization functions
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
