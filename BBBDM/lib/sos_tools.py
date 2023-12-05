import logging

import numpy as np
import pandas as pd

from lib.data_processing import *
from lib.Normalizing import *


def update_columns_sos_two(row: pd.Series) -> pd.Series:
    """
    Takes in a row of our dataframe with filled out values for row["BusinessNameCorrect"], row["BusinessAddressCorrect"],
    and row["BusinessZipCorrect"]

    Function makes sure we have matching name and address inorder to provide updated information

    Returns: updated row in the dataframe
    """
    if row["BusinessNameCorrect"] and row["AddressCorrect"]:
        row["BusinessNameUpdate"].append(row["Business Name"])
        row["BusinessNameFound"] = "SOS" if row["BusinessNameCorrect"] else np.nan
        row["AddressUpdate"].append(f"{row['Address New']}")
        row["AddressFound"] = "SOS" if row["AddressCorrect"] else np.nan
        row["ZipUpdate"].append(row["Zip Code New"])
        row["ZipFound"] = "SOS" if row["ZipCorrect"] else np.nan
    else:
        row["BusinessNameCorrect"] = False
        row["AddressCorrect"] = False

    logging.info(
        f'Updated row with business name: {row["BusinessNameUpdate"]} from truth source: {row["BusinessNameFound"]}'
    )

    return row


def update_sos_columns_one(row: pd.Series) -> pd.Series:
    """
    Calculates if our data is correct or not when compared to SOS (Secretary of State).
    Sets null values for other columns and performs additional data processing.

    This function takes a DataFrame containing business data and compares it to Secretary of State (SOS) records to assess the correctness of the data. It adds several columns to the DataFrame to indicate whether specific fields like Business Name, Address, and Zip Code match SOS records.

    It also sets null values for additional columns, which are intended to be filled out during further processing.

    Parameters:
        merged_data (pd.DataFrame): The input DataFrame containing business data.

    Returns:
        pd.DataFrame: A modified DataFrame with added columns and null values, ready for further processing.
    """
    business_matches = False
    address_matches = False

    for name in row["BusinessName"]:
        if not isinstance(row["Business Name"], str):
            break
        if is_same_business(name, row["Business Name"], 80, "", "a", True):
            business_matches = True

    # If address matches OR city matches, assume correct
    for address in row["Address"]:
        if not isinstance(row["Address New"], str):
            break
        if address_match_found(address, row["Address New"]):
            address_matches = True

    row["BusinessNameCorrect"] = business_matches
    row["AddressCorrect"] = address_matches
    if isinstance(row["Zip Code New"], str):
        row["ZipCorrect"] = row["Zip Code New"] in row["Zipcode"]
    else:
        row["ZipCorrect"] = False

    row = update_columns_sos_two(row)
    return row


def add_sos_columns(data: pd.DataFrame) -> pd.DataFrame:
    # Give null values for all columns, which we will fill out when needed
    data["BusinessNameCorrect"] = False
    data["BusinessNameUpdate"] = [[] for _ in range(len(data))]
    data["BusinessNameFound"] = np.nan
    data["AddressCorrect"] = False
    data["AddressUpdate"] = [[] for _ in range(len(data))]
    data["AddressFound"] = np.nan
    data["ZipCorrect"] = False
    data["ZipUpdate"] = [[] for _ in range(len(data))]
    data["ZipFound"] = np.nan
    data["PhoneCorrect"] = False
    data["PhoneUpdate"] = [[] for _ in range(len(data))]
    data["PhoneFound"] = np.nan
    data["EmailCorrect"] = False
    data["EmailUpdate"] = [[] for _ in range(len(data))]
    data["EmailFound"] = np.nan
    data["WebsiteCorrect"] = False
    data["WebsiteUpdate"] = [[] for _ in range(len(data))]
    data["WebsiteFound"] = np.nan

    return data


def add_update_columns(data: pd.DataFrame) -> pd.DataFrame:
    data["Business Name"] = np.nan
    data["Address New"] = np.nan
    data["Zip Code New"] = np.nan
    data["City"] = np.nan

    return data


def compare_dataframes_sos(
    historicalData: pd.DataFrame, newData: pd.DataFrame
) -> pd.DataFrame:
    """
    Compares old data to new, deleting duplicate rows, and adding the necessary columns
     Parameters:
        historicalData (pd.DataFrame): The historical data DataFrame.
        newData (pd.DataFrame): The new data DataFrame containing Secretary of State information.

    Returns: Dataframe containing updated information from SOS
    """

    if newData.empty:
        raise ValueError(
            "The SOS dataframe is empty, check file to ensure contents present"
        )

    historicalData.rename(columns={"Firm_Id": "firm_id"}, inplace=True)

    columns_to_update = ["Business Name", "Address 1", "Zip Code New", "City"]
    historicalData = add_update_columns(historicalData)

    sos_names = list(newData["Business Name"])
    sos_names_normal = standardizeName(list(newData["Business Name"]), is_sos=True)
    mapping = {
        normalized_value: original_value
        for original_value, normalized_value in zip(sos_names, sos_names_normal)
    }

    # Loop over each historical row
    for his_idx, his_row in historicalData.iterrows():
        # Extract list of business names
        row_names = his_row["BusinessName"]
        # Loop over list of names
        for name in row_names:
            name = normalize_name(name)
            # Check if we have a match in sos_data
            if name in sos_names_normal:
                # Find the row in sos_data
                sos_update_row = newData[
                    newData["Business Name"] == mapping[name]
                ].head(1)
                # Shape dataframe into row, since we know there is a 1-1 mapping
                sos_update_row = sos_update_row.squeeze(axis=0)

                # Now, update the columns in the historical dataframe, these will be used for comparing
                historicalData.loc[his_idx, "Business Name"] = sos_update_row[
                    "Business Name"
                ]
                historicalData.loc[
                    his_idx, "Address New"
                ] = f"{sos_update_row['Address 1']}, {sos_update_row['City']}, {sos_update_row['Zip Code']}"
                historicalData.loc[his_idx, "Zip Code New"] = sos_update_row["Zip Code"]
                historicalData.loc[his_idx, "City"] = sos_update_row["City"]

                break

    try:
        historicalData = add_sos_columns(historicalData)
        historicalData = historicalData.apply(update_sos_columns_one, axis=1)
        logging.info("Columns for SOS have been added - Success")
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when adding columns".format(e))
        return False

    # Select the desired columns
    result_df = historicalData[
        [
            "firm_id",
            "BusinessName",
            "BusinessNameCorrect",
            "BusinessNameUpdate",
            "BusinessNameFound",
            "Phone",
            "PhoneCorrect",
            "PhoneUpdate",
            "PhoneFound",
            "Website",
            "WebsiteCorrect",
            "WebsiteUpdate",
            "WebsiteFound",
            "Email",
            "EmailCorrect",
            "EmailUpdate",
            "EmailFound",
            "City",
            "Address",
            "AddressCorrect",
            "AddressUpdate",
            "AddressFound",
            "Zipcode",
            "ZipCorrect",
            "ZipUpdate",
            "ZipFound"
            # Optional output columns
            # 'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code', 'Party Full Name',
            # 'Next Renewal Due Date'
        ]
    ]

    return result_df
