import pandas as pd
import logging

from BBBDM.lib.data_processing import *
from BBBDM.lib.google_places_tools import *
from BBBDM.lib.sos_tools import *
from BBBDM.lib.Normalizing import *
from BBBDM.lib.yellow_pages_tools import *

pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


def main():
    # Extract the data
    # Need to build a function which takes in a file path for a csv file, and outputs a dataframe
    mn_business = get_valid_businesses_info("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business.csv")
    mn_business_address = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_address.csv")
    mn_business_contact = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_contact.csv")
    mn_business_email = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_email.csv")
    mn_business_name = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_name.csv")
    mn_business_phone = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_phone.csv")
    mn_business_url = extract_data("/Users/collindahlback/Library/Mobile Documents/com~apple~CloudDocs/Spring2023/CSParallel/BBB/BBBDM/Data/mn_business_url.csv")

    # Merge the data
    merged_data = join_dataframe_firmid(mn_business, mn_business_address, mn_business_contact, mn_business_email,
                                        mn_business_name, mn_business_phone, mn_business_url)

    # Create valid/invalid dataframes
    valid_data, invalid_data = filter_dataframes(merged_data)

    # Standardize the valid data
    valid_data = normalize_dataframe(valid_data)
    invalid_data = normalize_dataframe(invalid_data)

    # Compare to SOS, updating when necessary
    path_to_sos = ""
    SOS_data = extract_data(path_to_sos)
    valid_data = compare_dataframes_sos(valid_data, SOS_data)

    # Compare to Google API
    
    # Compare to YP

    # Merge with bad data

    # Output csv
    pass


if __name__ == "__main__":
    main()