import re
import logging

# Configure logging
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


# Normalize Email
def normalize_email(email:str) -> str | None:
    """
    Normalize email addresses by converting to lowercase, removing whitespace, and removing special characters
    except ., @, and -. If the email address does not contain an @ symbol, it is considered invalid and None is
    
    Parameters:
    email: Email address to normalize
    
    Returns:
    Normalized email address or None if invalid
    """
    email = email.lower()  # Convert to lowercase
    email = re.sub(r'\s', '', email)  # Remove whitespace
    email = re.sub(r'[^a-z0-9.@-]', '', email)  # Remove special characters except ., @, and -
    if '@' not in email:
        logging.warning(f'Invalid email: {email}')
        return None  # Invalid email
    return email

# Normalize Phone Number
def normalize_phone_number(phone:str) -> str | None:
    """
    Normalize phone numbers by removing whitespace and non-numeric characters. If the phone number does not
    contain any numeric digits, it is considered invalid and None is returned.

    Parameters:
    phone: Phone number to normalize

    Returns:
    Normalized phone number or None if invalid
    """
    if not any(char.isdigit() for char in phone):  # Check if there are no numeric digits in the phone number
        logging.warning(f'Invalid phone number: {phone}')
        return None  # Invalid phone number
    phone = re.sub(r'\s|\D', '', phone)  # Remove whitespace and non-numeric characters
    return phone

# Normalize Zipcode
def normalize_zipcode(zipcode:str) -> str | None:
    """
    Normalize zipcodes by removing whitespace and non-numeric characters. If the zipcode does not contain
    exactly 5 numeric digits, it is considered invalid and None is returned.

    Parameters:
    zipcode: Zipcode to normalize

    Returns:
    Normalized zipcode or None if invalid
    """
    zipcode = re.sub(r'\s|\D', '', zipcode)  # Remove whitespace and non-numeric characters
    if len(zipcode) == 5:
        return zipcode
    else:
        logging.warning(f'Invalid zipcode: {zipcode}')
        return None  # Invalid zipcode

# Define a function to normalize the entire DataFrame
def normalize_dataframe(df:pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the entire DataFrame by applying the normalize_email, normalize_phone_number, and normalize_zipcode
    functions to the Email, Phone Number, and Zipcode columns respectively. Invalid values are replaced with None.

    Parameters:
    df: DataFrame to normalize

    Returns:
    Normalized DataFrame
    """
    # Apply each normalization function to respective columns
    df['Email'] = df['Email'].apply(normalize_email)
    df['Phone Number'] = df['Phone Number'].apply(normalize_phone_number)
    df['Zipcode'] = df['Zipcode'].apply(normalize_zipcode)

    return df


