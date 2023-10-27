import pandas as pd
import logging

logging.basicConfig(filename='matching_address.log', level=logging.DEBUG)

def address_match_found(historical_addresses, found_addresses):
    """
    Function to compare historical and new addresses and determine if they match.
    Returns a new DataFrame with a 'match_found' column containing 1 for a match, 2 for matching cities, and 0 for no match.
    Also adds a 'city_match_name' column to show the city name when match_found is 2.
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

        return merged_df
    except Exception as e:
        logging.debug(f"Error occurred: {e}")
        return False

