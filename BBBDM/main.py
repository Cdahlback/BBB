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
 
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from lib.data_processing import (
    extract_data,
    filter_dataframes,
    get_valid_businesses_info,
    join_dataframe_firmid,
)
from lib.google_places_tools import google_validation
from lib.Normalizing import normalize_dataframe
from lib.sos_tools import compare_dataframes_sos
from lib.yellow_pages_tools import update_dataframe_with_yellow_pages_data
from pandarallel import pandarallel
pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename="functions.log", level=logging.DEBUG)
# Loads the .env file
ENV_PATH = str(Path(__file__).parent.parent / ".env")
load_dotenv(dotenv_path=ENV_PATH)
pandarallel.initialize(progress_bar=True)

def main():
    """
    Function which sets up our environment variables and runs the system
    """
    # Extract the data
    mn_business = get_valid_businesses_info((str(Path(__file__).parent / "Data/mn_business.csv"))).head(100)
    mn_business_address = extract_data((str(Path(__file__).parent / "Data/mn_business_address.csv"))).head(100)
    mn_business_email = extract_data((str(Path(__file__).parent / "Data/mn_business_email.csv"))).head(100)
    mn_business_name = extract_data((str(Path(__file__).parent / "Data/mn_business_name.csv"))).head(100)
    mn_business_phone = extract_data((str(Path(__file__).parent / "Data/mn_business_phone.csv"))).head(100)
    mn_business_url = extract_data((str(Path(__file__).parent / "Data/mn_business_url.csv"))).head(100)

    # Merge the data
    merged_data = join_dataframe_firmid(
        mn_business,
        mn_business_address,
        mn_business_email,
        mn_business_name,
        mn_business_phone,
        mn_business_url,
    )

    # Create valid/invalid dataframes
    valid_data, invalid_data = filter_dataframes(merged_data)

    # Standardize the valid data
    valid_data = normalize_dataframe(valid_data)
    invalid_data = normalize_dataframe(invalid_data)

    # Compare to SOS, updating when necessary
    path_to_sos = (str(Path(__file__).parent / "Data/sos_data.csv"))
    SOS_data = extract_data(path_to_sos)
    valid_data = compare_dataframes_sos(valid_data, SOS_data)

    # Compare to Google API
    valid_data = valid_data.parallel_apply(google_validation, axis=1)
    # Compare to YP
    valid_data = update_dataframe_with_yellow_pages_data(valid_data)
    # Merge with bad data

    #Print the data to csv
    valid_data.to_csv(str(Path(__file__).parent / "Data/valid_data.csv"))
    invalid_data.to_csv(str(Path(__file__).parent / "Data/invalid_data.csv")) 

    logging.info("Data has been printed to csv - Success")


if __name__ == "__main__":
    main()
