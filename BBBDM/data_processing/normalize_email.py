
import logging
#pip install email-validator
from email_validator import validate_email, EmailNotValidError
import pandas as pd

# Configure logging
logging.basicConfig(filename='normalize_email.log', level=logging.DEBUG)

# Normalize email
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

# normalize_dataframe function to normalize the entire DataFrame
def normalize_dataframe(df:pd.DataFrame) ->pd.DataFrame:
    # Apply the normalize_email function to the 'email' column
    df['email'] = df['email'].apply(normalize_email)
    return df # Return the modified DataFrame