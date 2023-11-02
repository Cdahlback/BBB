"""
Function to abstract all code into simple steps
Step1: Extract the Data from different sources
Step2: Merge the extracted dataframes
Step3: Segregate valid/invalid data into their own dataframes
Step4: Normalize both dataframes
Step5: Compare our data to SOS
Step6: Compare data NOT validated by SOS to Google Places
Step7: Compare data NOT validated by SOS or Google places to Yellow pages
Step8: Merge the data back with the invalid and unverified data
Step9: Output results to csv file
"""

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
    """
    Function which sets up our environment variables and runs the system
    """
    # Extract the data
    mn_business = get_valid_businesses_info("Data/mn_business.csv")
    mn_business_address = extract_data("Data/mn_business_address.csv")
    mn_business_contact = extract_data("Data/mn_business_contact.csv")
    mn_business_email = extract_data("Data/mn_business_email.csv")
    mn_business_name = extract_data("Data/mn_business_name.csv")
    mn_business_phone = extract_data("Data/mn_business_phone.csv")
    mn_business_url = extract_data("Data/mn_business_url.csv")

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
    # TODO: Get chris's pull request merged

    # Compare to YP
    valid_data = update_dataframe_with_yellow_pages_data(valid_data)
    # Merge with bad data

    # Output csv
    pass


if __name__ == "__main__":
    main()