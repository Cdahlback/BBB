import re
import logging

# Configure logging
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


# Normalize Email
def normalize_email(email):
    email = email.lower()  # Convert to lowercase
    email = re.sub(r'\s', '', email)  # Remove whitespace
    email = re.sub(r'[^a-z0-9.@-]', '', email)  # Remove special characters except ., @, and -
    if '@' not in email:
        logging.warning(f'Invalid email: {email}')
        return None  # Invalid email
    return email

# Normalize Phone Number
def normalize_phone_number(phone):
    if not any(char.isdigit() for char in phone):  # Check if there are no numeric digits in the phone number
        logging.warning(f'Invalid phone number: {phone}')
        return None  # Invalid phone number
    phone = re.sub(r'\s|\D', '', phone)  # Remove whitespace and non-numeric characters
    return phone

# Normalize Zipcode
def normalize_zipcode(zipcode):
    zipcode = re.sub(r'\s|\D', '', zipcode)  # Remove whitespace and non-numeric characters
    if len(zipcode) == 5:
        return zipcode
    else:
        logging.warning(f'Invalid zipcode: {zipcode}')
        return None  # Invalid zipcode

# Define a function to normalize the entire DataFrame
def normalize_dataframe(df):
    # Apply each normalization function to respective columns
    df['Email'] = df['Email'].apply(normalize_email)
    df['Phone Number'] = df['Phone Number'].apply(normalize_phone_number)
    df['Zipcode'] = df['Zipcode'].apply(normalize_zipcode)

    return df


