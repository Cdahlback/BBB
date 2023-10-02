import pandas as pd
import logging

pd.options.mode.chained_assignment = None  # Disable the warning
logging.basicConfig(filename='functions.log', level=logging.DEBUG)


def compare_dataframes(historicalData: pd.DataFrame, newData: pd.DataFrame) -> pd.DataFrame:

    left_on = "BusinessName"
    right_on = "Business Name"
    try:
        # Merge historicalData and newData on the 'BusinessName' column
        merged_data = historicalData.merge(newData, left_on=left_on, right_on=right_on, how='inner')
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when merging historicalData with secretary of state".format(e))
        logging.debug("Length historical data: {0}".format(len(historicalData)))
        logging.debug("Length new data: {0}".format(len(newData)))
        return False

    try:
        # Calculate MatchesAddress and MatchesZip
        merged_data['MatchesAddress'] = merged_data['Address'] == merged_data['Address 1']
        merged_data['MatchesZip'] = merged_data['Zip Code_x'] == merged_data['Zip Code_y']
    except KeyError as e:
        logging.debug("Exception: KeyError {0} occurred when accessing merged_data (historical/secretary)".format(e))
        return False

    # Select the desired columns
    result_df = merged_data[['Firm_id', 'BusinessName', 'MatchesAddress', 'Address 1', 'MatchesZip', 'Zip Code_y',
                            'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code',
                            'Party Full Name', 'Next Renewal Due Date']]

    # Rename columns for clarity
    result_df.rename(columns={'Address 1': 'Address_new', 'Zip Code_y': 'Zip Code_new'}, inplace=True)
    logging.info("historicalData has been merged with Secretary Of State data Successfully")

    return result_df
