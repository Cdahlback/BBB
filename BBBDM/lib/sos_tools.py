import logging
import pandas as pd


def update_columns_sos(row: pd.Series) -> pd.Series:
    """
    Takes in a row of our dataframe with filled out values for row["BusinessNameCorrect"], row["BusinessAddressCorrect"],
    and row["BusinessZipCorrect"]

    Function makes sure we have matching name and address inorder to provide updated information

    Returns: updated row in the dataframe
    """
    if row["BusinessNameCorrect"] and row["BusinessAddressCorrect"]:
        row["BusinessNameUpdate"] = row["Business Name"]
        row["BusinessNameFound"] = "SOS" if not pd.isna(row["BusinessNameUpdate"]) else np.nan

        # Add address columns
        row["BusinessAddressUpdate"] = row["Address 1"]
        row["BusinessAddressFound"] = "SOS" if not pd.isna(row["BusinessAddressUpdate"]) else np.nan

        # Add zip columns
        row["BusinessZipUpdate"] = row["Zip Code New"]
        row["BusinessZipFound"] = "SOS" if not pd.isna(row["BusinessZipUpdate"]) else np.nan

        logging.info(f'Updated row with business name: {row["BusinessNameUpdate"]} from truth source: {row["BusinessNameFound"]}')

    return row


def add_sos_columns(merged_data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates if our data is correct or not when compared to SOS
    sets null values for other columns
    """
    # See if the business name and address match
    merged_data["BusinessNameCorrect"] = merged_data["BusinessName"] == merged_data["Business Name"]
    merged_data["BusinessAddressCorrect"] = merged_data["Address"] == merged_data["Address 1"]
    merged_data["BusinessZipCorrect"] = merged_data["Zip Code"] == merged_data["Zip Code New"]

    # Give null values for all columns, which we will fill out when needed
    merged_data["BusinessNameUpdate"] = np.nan
    merged_data["BusinessNameFound"] = np.nan
    merged_data["BusinessAddressUpdate"] = np.nan
    merged_data["BusinessAddressFound"] = np.nan
    merged_data["BusinessZipUpdate"] = np.nan
    merged_data["BusinessZipFound"] = np.nan

    merged_data.apply(update_columns_sos, axis=1)

    return merged_data


def compare_dataframes_sos(historicalData: pd.DataFrame, newData: pd.DataFrame) -> pd.DataFrame:
    """
    Compares old data to new, deleting duplicate rows, and adding the necessary columns

    Returns: Dataframe containing updated information from SOS
    """
    left_on = "BusinessName"
    right_on = "Business Name"

    try:
        # Merge the data, keeping all values from historicalData rows from newData where BusinessNames match
        merged_data = historicalData.merge(newData, left_on=left_on, right_on=right_on, how='inner')
        merged_data = pd.concat([historicalData, merged_data], ignore_index=True)

        # Drop duplicate rows which contain no updated information
        merged_data['is_duplicate'] = merged_data.duplicated(subset='Firm_id', keep=False)
        merged_data = merged_data[(merged_data['is_duplicate'] & merged_data['Business Name'].notna()) | (~merged_data['is_duplicate'])]
        merged_data.drop(columns=['is_duplicate'], inplace=True)
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when merging historicalData with secretary of state".format(e))
        logging.debug("Length historical data: {0}".format(len(historicalData)))
        logging.debug("Length new data: {0}".format(len(newData)))
        return False

    try:
        add_sos_columns(merged_data)
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when accessing merged_data (historical/secretary)".format(e))
        return False

    # Select the desired columns
    result_df = merged_data[[
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound'
        # Optional output columns
        # 'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code', 'Party Full Name',
        # 'Next Renewal Due Date'
    ]]

    logging.info("historicalData has been merged with Secretary Of State data Successfully")
    return result_df