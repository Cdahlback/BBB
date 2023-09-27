import pandas as pd


def compare_dataframes(historicalData: pd.DataFrame, newData: pd.DataFrame) -> pd.DataFrame:
    if historicalData.empty or newData.empty:
        result_df = pd.DataFrame(columns=['Firm_id', 'BusinessName', 'MatchesAddress', 'Address_new', 'MatchesZip', 'Zip Code_new',
                            'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code',
                            'Party Full Name', 'Next Renewal Due Date'])
        return result_df

    # Merge historicalData and newData on the 'BusinessName' column
    merged_data = historicalData.merge(newData, left_on='BusinessName', right_on='Business Name', how='inner')

    # Calculate MatchesAddress and MatchesZip
    merged_data['MatchesAddress'] = merged_data['Address'] == merged_data['Address 1']
    merged_data['MatchesZip'] = merged_data['Zip Code_x'] == merged_data['Zip Code_y']

    # Select the desired columns
    result_df = merged_data[['Firm_id', 'BusinessName', 'MatchesAddress', 'Address 1', 'MatchesZip', 'Zip Code_y',
                            'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code',
                            'Party Full Name', 'Next Renewal Due Date']]

    # Rename columns for clarity
    result_df.rename(columns={'Address 1': 'Address_new', 'Zip Code_y': 'Zip Code_new'}, inplace=True)

    return result_df
