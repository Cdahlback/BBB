import pandas as pd
import logging

# Configure logging
logging.basicConfig(filename='functions.log', level=logging.DEBUG)

pd.options.mode.chained_assignment = None  # Disable the warning

def get_valid_businesses_info(file_name):
    try:
        # Read the data from the specified file into a DataFrame
        df = pd.read_csv(file_name)
        
        # Ensure the "active" column is treated as a string
        df['active'] = df['active'].astype(str)

        # Filter the DataFrame to only keep rows where 'active' == 'TRUE'
        active_businesses_df = df[df['active'].str.strip().str.upper() == 'TRUE']

        # Log success message
        logging.info(f"Successfully read and filtered data from file: {file_name}")

        # Only return business information for the active businesses
        return active_businesses_df
    except Exception as e:
        # Log error message
        logging.error(f"Error reading or filtering data from file: {file_name}. Error: {e}")
        return None

# Specify the relative file path based on the script's location
file_name = r'C:\Users\Rania\Documents\GitHub\BBB\BBBDM\Data\mn_business.csv'

# Call the function with the relative file path
active_businesses_info = get_valid_businesses_info(file_name)
