import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='functions.log', level=logging.DEBUG)

pd.options.mode.chained_assignment = None  # Disable the warning

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
