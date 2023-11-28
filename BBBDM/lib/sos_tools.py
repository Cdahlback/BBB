import logging

import numpy as np
import pandas as pd

from BBBDM.lib.data_processing import address_match_found, is_same_business


def update_columns_sos_two(row: pd.Series) -> pd.Series:
    """
    Takes in a row of our dataframe with filled out values for row["BusinessNameCorrect"], row["BusinessAddressCorrect"],
    and row["BusinessZipCorrect"]

    Function makes sure we have matching name and address inorder to provide updated information

    Returns: updated row in the dataframe
    """
    if row["BusinessNameCorrect"] and row["BusinessAddressCorrect"]:
        row["BusinessNameUpdate"] = row["Business Name"]
        row["BusinessNameFound"] = (
            "SOS" if not pd.isna(row["BusinessNameUpdate"]) else np.nan
        )

        # Add address columns
        row["BusinessAddressUpdate"] = row["Address 1"]
        row["BusinessAddressFound"] = (
            "SOS" if not pd.isna(row["BusinessAddressUpdate"]) else np.nan
        )

        # Add zip columns
        row["BusinessZipUpdate"] = row["Zip Code New"]
        row["BusinessZipFound"] = (
            "SOS" if not pd.isna(row["BusinessZipUpdate"]) else np.nan
        )

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
    # If address matches OR city matches, assume correct
    for name in row["BusinessName"]:
        if is_same_business(name, row["Business Name"], 80, "", "a", True):
            row['BusinessNameCorrect'] = True
            break

    for address in row["Address"]:
        if address_match_found(address, row["Address 1"]):
            row["BusinessAddressCorrect"] = True
            break

    row["BusinessZipCorrect"] = (row["Zip Code"] == row["Zip Code New"])

    row = update_columns_sos_two(row)
    logging.info("add_sos_columns function executed successfully")
    return row


def add_sos_columns(data: pd.DataFrame) -> pd.DataFrame:
    # Give null values for all columns, which we will fill out when needed
    data["BusinessNameCorrect"] = False
    data["BusinessNameUpdate"] = np.nan
    data["BusinessNameFound"] = np.nan
    data["BusinessAddressCorrect"] = False
    data["BusinessAddressUpdate"] = np.nan
    data["BusinessAddressFound"] = np.nan
    data["BusinessZipCorrect"] = False
    data["BusinessZipUpdate"] = np.nan
    data["BusinessZipFound"] = np.nan

    return data


def add_update_columns(data: pd.DataFrame) -> pd.DataFrame:
    data["Business Name"] = np.nan
    data["Address 1"] = np.nan
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
        raise ValueError("The SOS dataframe is empty, check file to ensure contents present")

    historicalData = add_update_columns(historicalData)

    for _, new_row in newData.iterrows():
        try:
            sos_name = new_row["Business Name"]
            sos_address = new_row["Address 1"]
            sos_zip = new_row["Zip Code New"]
            sos_city = new_row["City"]
        except ValueError as e:
            print(e)
            raise ValueError()

        for his_idx, his_row in historicalData.iterrows():
            if sos_name in his_row["BusinessName"]:
                his_row["Business Name"] = sos_name
                his_row["Address 1"] = sos_address
                his_row["Zip Code New"] = sos_zip
                his_row["City"] = sos_city
                historicalData.loc[his_idx] = his_row
                print(historicalData)

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
            "Firm_id",
            "BusinessName",
            "BusinessNameCorrect",
            "BusinessNameUpdate",
            "BusinessNameFound",
            "Address",
            "BusinessAddressCorrect",
            "BusinessAddressUpdate",
            "BusinessAddressFound",
            "Zip Code",
            "BusinessZipCorrect",
            "BusinessZipUpdate",
            "BusinessZipFound"
            # Optional output columns
            # 'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code', 'Party Full Name',
            # 'Next Renewal Due Date'
        ]
    ]

    return result_df
