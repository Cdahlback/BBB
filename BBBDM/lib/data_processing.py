"""
Mine
"""
import numpy as np
import pandas as pd
import logging
from functools import reduce
from email_validator import validate_email, EmailNotValidError
from fuzzywuzzy import fuzz

logging.basicConfig(filename='functions.log', level=logging.DEBUG)

def join_dataframe_firmid(*data_frames:pd.DataFrame) -> pd.DataFrame:
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
    Filter the DataFrame based on the following conditions:
     Rows are automatically invalid if the 'name" column is null or empty.
     Rows are valid if they have a non- empty 'name' and at least one other 
     non- empty column

    """
    valid_rows = []
    invalid_rows = []

    # Loop through each row in the dataframe. "idx" is the index of the row, and "row" is the data in the row

    for idx, row in df.iterrowas():
        # Check ifthe 'name' column in the current row is null or empty  
        if pd.isna(row['name']) or row['name'] == '':
            invalid_rows.append(idx) # If the name is missing, append the index to the invalid_rows list
            continue #skip the rest of the current loop iteration

        # I nitialize a counter to count the number of non-empty data types excluding 'name'
        counter = 0

        for column in ['address', 'iphone', 'website', 'email']:
            # Check if the current column's data is not null and not empty

            if not pd.isna(row[column]) and row[column] != '':
                counter += 1 # Increment the counter if the column's data is non- empty


        # Check if the counter( number of non-rmpty columns) is greater than xero
        if counter > 0:
         valid_rows.append(idx) #iF YES, THE row is valid. Append the index to the invalid_rows list
        
        else:
            valid_rows.append(idx) #iF YES, THE row is valid. Append the index to the invalid_rows list
    # create a new Dateframe using the indices of valid rows
    valid_df = df.loc[valid_rows]
    # create a new Dataframe using the indices of invalid rows
    invalid_df = df.loc[invalid_rows]

    #Return the two Datafroma: valid_df and invalid_df
    return valid_df, invalid_df


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


def is_same_business(historical_name: str, new_name: str, threshold: int = 80,
                     business_type_historical: str = None, business_type_new: str = None,
                     is_SOS: bool = False) -> bool:
    """
    Check if the new business name is essentially the same as the historical one.
    Uses fuzzy string matching to make this determination. If the names are not from SOS,
    removes common business suffixes before comparing.
    """

    # Helper function to preprocess names
    def preprocess_name(name: str) -> str:
        # Convert to lowercase
        name = name.lower()

        # If not from SOS, remove common business suffixes
        for suffix in ["inc", "llc", "ltd", "co", ".", ",", "&", "corp", "incorporation"]:
            name = name.replace(suffix, "")

        return name.strip()

    # If not from SOS, preprocess the business names"
    if not is_SOS:
        historical_name = preprocess_name(historical_name)
        new_name = preprocess_name(new_name)

    # If business types are provided and they don't match, return False immediately
    if business_type_historical and business_type_new and business_type_historical != business_type_new:
        return False

    # Token match ratio
    token_ratio = fuzz.token_sort_ratio(historical_name, new_name)

    # Regular fuzzy match ratio
    fuzzy_ratio = fuzz.ratio(historical_name, new_name)

    # Partial match ratio
    partial_ratio = fuzz.partial_ratio(historical_name, new_name)

    # Return True if any of the above ratios exceed the threshold
    return any(ratio >= threshold for ratio in [token_ratio, fuzzy_ratio, partial_ratio])


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

def get_valid_businesses_info(file_path:str) -> pd.DataFrame:
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
