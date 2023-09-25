import pandas as pd


def compare_dataframes(historicalData, newData):
    # Initialize an empty result dataframe
    result_df = pd.DataFrame(columns=[
        'PrimaryKey', 'BusinessNameMatch', 'BusinessName', 'EmailMatch', 'Email', 'PhoneMatch', 'Phone',
        'AddressMatch', 'Address', 'WebsiteMatch', 'Website'
    ])

    if len(historicalData) < 1 or len(newData) < 1:
        return result_df

    # Iterate through rows of historicalData
    for index, row in historicalData.iterrows():
        primary_key = row['PrimaryKey']
        business_name = row['BusinessName']
        email = row['Email']
        phone = row['Phone']
        address = row['Address']
        website = row['Website']

        # Check if the PrimaryKey exists in newData
        if primary_key in newData['PrimaryKey'].values:
            new_row = {'PrimaryKey': primary_key,
                        # Check if BusinessName matches
                       'BusinessNameMatch': business_name == newData.loc[newData['PrimaryKey'] == primary_key, 'BusinessName'].values[0],
                       'BusinessName': newData.loc[newData['PrimaryKey'] == primary_key, 'BusinessName'].values[0],
                        # Check if Email matches
                       'EmailMatch': email == newData.loc[newData['PrimaryKey'] == primary_key, 'Email'].values[0],
                       'Email': newData.loc[newData['PrimaryKey'] == primary_key, 'Email'].values[0],
                        # Check if Phone matches
                       'PhoneMatch': phone == newData.loc[newData['PrimaryKey'] == primary_key, 'Phone'].values[0],
                       'Phone': newData.loc[newData['PrimaryKey'] == primary_key, 'Phone'].values[0],
                        # Check if Address matches
                       'AddressMatch': address == newData.loc[newData['PrimaryKey'] == primary_key, 'Address'].values[
                           0],
                       'Address': newData.loc[newData['PrimaryKey'] == primary_key, 'Address'].values[0],
                        # Check if Website matches
                       'WebsiteMatch': website == newData.loc[newData['PrimaryKey'] == primary_key, 'Website'].values[
                           0],
                       'Website': newData.loc[newData['PrimaryKey'] == primary_key, 'Website'].values[0]}

            # Append the row to the result dataframe
            result_df = result_df.append(new_row, ignore_index=True)

    return result_df
