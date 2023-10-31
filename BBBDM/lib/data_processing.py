import numpy as np
import pandas as pd
from email_validator import validate_email, EmailNotValidError
"""
Mine
"""
import pandas as pd
import logging
from functools import reduce

logging.basicConfig(filename='functions.log', encoding='utf-8', level=logging.DEBUG)

def join_dataframe_firmid(*data_frames:pd.DataFrame) -> pd.DataFrame | bool:
    """
    Pass in dataframes and merge them on the FirmID column
    Remove any duplicate columns also

    Parameters:
    data_frames (pd.DataFrame): Dataframes to merge

    Returns:
    pd.DataFrame | bool: Returns a dataframe if successful, False if not
    """
    #Checks if there are any dataframes to merge
    if len(data_frames) == 0:
        logging.debug("No dataframes to merge")
        return False
    #Checks if there is only one dataframe to merge
    elif len(data_frames) < 2:
        logging.debug("Not enough dataframes to merge")
        return data_frames[0]
    #Checks if the dataframes have FirmID
    try:
        x = data_frames[0]['FirmID']
    except Exception as e:
        logging.exception(e)
        logging.exception("Did the dataframes have FirmID?")
        return False
    logging.debug("Dataframe contains FirmID - Success")
    #Merges multiple dataframes on FirmID via the amazing reduce function and the merge with the lambda to iterate over it
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['FirmID'], how='outer'), data_frames)
    logging.debug("Merging dataframes - Success")
    #Removes duplicate columns
    df = df_merged.loc[:,~df_merged.columns.duplicated()]
    logging.debug("Removing duplicate columns - Success")
    return df

def extract_data(file_path: str) -> pd.DataFrame:
    """
    Read the data from the specified file into a DataFrame

    Parameters:
    file_path: Relative path to the file to read

    Returns:
    DataFrame containing information for the businesses or None if an error occurs
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        # Log error message
        print(f"Error reading data from file: {file_path}. Error: {e}")
        return None


# Define the function to concatenate Address 1 and City
def concat_address(row: pd.Series) -> pd.Series:
    """
    Takes in a row and concats the address with the city. This allows our matching algo to work with addresses.

    Parameters:
    row: Row which we want to modify

    Returns: concatination of address 1 and city OR np.nan if fail to concat (values are np.nan)

    How to use:
    df['Address'] = df.apply(concat_address, axis=1)
    """
    if pd.notna(row['Address 1']) and pd.notna(row['city']):
        return row['Address 1'] + ', ' + row['city']
    else:
        return np.nan
def filter_dataframes(df:pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Filter the DataFrame to only keep rows where at least one of the following conditions is true:
    - name is not null and not empty
    - address is not null and not empty
    - phone is not null and matches the pattern for a phone number
    - website is not null and not empty
    - email is not null and not empty

    Parameters:
    df: DataFrame to filter

    Returns:
    Tuple of DataFrames containing the valid and invalid rows respectively
    """
    conditions = (
        ((df['name'].notna() & (df['name'] != '')) |
         (df['address'].notna() & (df['address'] != '')) |
         (df['phone'].notna() & df['phone'].str.match(r'^\d{10}$')) |
         (df['website'].notna() & (df['website'] != '')) |
         (df['email'].notna() & (df['email'] != ''))
        )
    )

    valid_df = df[conditions]
    invalid_df = df[~conditions]

    # Log information about the valid and invalid DataFrames
    logging.info("Valid DataFrame:\n%s", valid_df.to_string())
    logging.info("Invalid DataFrame:\n%s", invalid_df.to_string())

    return valid_df, invalid_df


df = pd.DataFrame({
    'name': ['John Doe', '', None],
    'address': ['123 Main St', '', None],
    'phone': ['1234567890', '123456789012', None],
    'website': ['www.example.com', '', None],
    'email': ['john.doe@example.com', '', None]
})

valid_df, invalid_df = filter_dataframes(df)



def address_match_found(historical_addresses, found_addresses):
    """
    Function to compare historical and new addresses and determine if they match.
    Returns a new DataFrame with a 'match_found' column containing 1 for a match, 2 for matching cities, and 0 for no match.
    Also adds a 'city_match_name' column to show the city name when match_found is 2.

    Parameters:
    Lists we want to merge into a dataframe
    Returns:
    a dataframe containing the historical address, the found address,the match_found and the city columns
    """
    try:
        # Create a DataFrame with only the historical and new address columns
        merged_df = pd.DataFrame({'historical_address': historical_addresses, 'found_address': found_addresses})

        def compare_addresses(row):
            if row['historical_address'] == row['found_address']:
                return 1
            elif row['historical_address'].split(',')[-1].strip() == row['found_address'].split(',')[-1].strip():
                return 2
            else:
                return 0

        # Apply the compare_addresses function to each row to determine matches
        merged_df['match_found'] = merged_df.apply(compare_addresses, axis=1)

        # Add 'city_match_name' column using list comprehension
        merged_df['city_match_name'] = ['N/A' if match != 2 else address.split(',')[-1].strip() for match, address in zip(merged_df['match_found'], merged_df['found_address'])]
        logging.info("Successful merge ")
        return merged_df
    except Exception as e:
        logging.debug(f"Error occurred: {e}")
        return False
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

def get_valid_businesses_info(file_path:str) -> pd.DataFrame | None:
    """
    Read the data from the specified file into a DataFrame and filter the DataFrame to only keep rows where
    'active' == 'TRUE'. If an error occurs, None is returned.

    Parameters:
    file_path: Relative path to the file to read

    Returns:
    DataFrame containing information for the active businesses or None if an error occurs
    """
    try:
        # Read the data from the specified file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Ensure the "active" column is treated as a string
        df['active'] = df['active'].astype(str)

        # Filter the DataFrame to only keep rows where 'active' == 'TRUE'
        active_businesses_df = df[df['active'].str.strip().str.upper() == 'TRUE']

        # Log success message
        logging.info(f"Successfully read and filtered data from file: {file_path}")

        # Only return business information for the active businesses
        return active_businesses_df
    except Exception as e:
        # Log error message
        logging.error(f"Error reading or filtering data from file: {file_path}. Error: {e}")
        return None

# Specify the relative file path based on the script's location
file_path = r'C:\Users\Rania\Documents\GitHub\BBB\BBBDM\Data\mn_business.csv'

# Call the function with the relative file path
active_businesses_info = get_valid_businesses_info(file_path)