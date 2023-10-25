import logging
import pandas as pd
# Import the geocoders from geopy to perform geolocation
from geopy.geocoders import Nominatim

# Import the geodesic function from geopy for calculating distances
from geopy.distance import geodesic

# Configure logging to write log messages to the 'matching_address.log' file with a debug level
logging.basicConfig(filename='matching_address.log', level=logging.DEBUG)
# 'address_match_found' that takes historical and new addresses as input
def address_match_found(historical_addresses, found_addresses):
    try:
        # Create a geolocator using the Nominatim service with a user agent name
        geolocator = Nominatim(user_agent="address_matcher")

       #this are list of output
        historical_addresses = list(historical_addresses)
        found_addresses = list(found_addresses)

        # Create a DataFrame 'merged_df' with columns 'historical_address' and 'found_address'
        merged_df = pd.DataFrame({'historical_address': historical_addresses, 'found_address': found_addresses})

        # Define a nested function 'compare_addresses' that compares historical and found addresses
        def compare_addresses(row):
            try:
                # Standardize address formatting for comparison
                historical_address = row['historical_address'].strip().lower()
                found_address = row['found_address'].strip().lower()

                # Geocode the historical and found addresses to obtain location information
                location1 = geolocator.geocode(historical_address)
                location2 = geolocator.geocode(found_address)

                # Check if location information is available for both addresses
                if location1 is not None and location2 is not None:
                    # Get the latitude and longitude coordinates for both addresses
                    coords1 = (location1.latitude, location1.longitude)
                    coords2 = (location2.latitude, location2.longitude)

                    # Calculate the distance in miles between the two addresses
                    distance = geodesic(coords1, coords2).miles

                # Check if the historical and found addresses are an exact match
                if historical_address == found_address:
                    return 1, 'N/A'    # Return 1 for matching addresses and the distance

                # Check if the cities in historical and found addresses match
                elif historical_address.split(',')[-2] == found_address.split(',')[-2]:
                    return 2, distance    # Return 2 for matching cities and the distance

                # Return 0 for non-matching addresses and the distance
                return 0, 'N/A'
            except Exception as e:
                logging.debug(f"Error occurred: {e}")
                return False

        # Apply the 'compare_addresses' function to each row in 'merged_df'
        merged_df['match_found'], merged_df['distance'] = zip(*merged_df.apply(compare_addresses, axis=1))

        # Return the resulting DataFrame with match information and distances
        return merged_df
    except Exception as e:
        # Handle and log any exceptions that may occur
        logging.debug(f"Error occurred: {e}")
        return False

# Example usage
historical_addresses = ['123 Main St, Springfield, USA', '456 Pine St, Boston, USA', '283 Oxford St, Rochester, USA']
new_addresses = ['123 Main St, Springfield, USA', '456 Maple St, California, USA', '99 Court St, Rochester, USA']

merged_df = address_match_found(historical_addresses, new_addresses)

# Print the resulting DataFrame
print(merged_df)
