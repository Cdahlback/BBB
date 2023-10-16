import numpy as np
import pandas as pd
import pytest
from BBBDM.historical_functions.Collin import compare_dataframes_sos, \
    update_dataframe_with_yellow_pages_data  # Import your actual function here


# Define a test case for a passing case in compare_dataframes
def test_compare_dataframes_pass():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame({
        'Firm_id': [1, 2, 3],
        'BusinessName': ['XYZ Corp', 'LMN Ltd', 'ABC Inc'],
        'Active': [True, False, True],
        'Address': ['123 Main St', '789 Oak St', '456 Elm St'],
        'Zip Code': ['12345', '67890', '54321']
    })

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame({
        'Business Name': ['XYZ Corp', 'PQR Corp', 'ABC Inc'],
        'Address 1': ['123 Main St', '777 Maple St', '456 Elm St'],
        'Zip Code New': ['12345', '99999', '54321'],
        'Business Filing Type': ['Type A', 'Type B', 'Type C'],
        'Filing Date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'Status': ['Active', 'Inactive', 'Active'],
        'Address 2': ['Suite 100', '', 'Apt 2B'],
        'City': ['City1', 'City2', 'City3'],
        'Region Code': ['NY', 'CA', 'TX'],
        'Party Full Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Next Renewal Due Date': ['2023-01-01', '2023-02-02', '2023-03-03']
    })

    # Call your function to find matching datapoints
    result_df = compare_dataframes_sos(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Check if the result has the expected columns
    expected_columns = [
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound'
    ]

    assert result_df.columns.tolist() == expected_columns


# Define a test case for a failing case in compare_dataframes
def test_compare_dataframes_fail():
    # Create two sample DataFrames with non-overlapping data
    historicalData = pd.DataFrame({
        'Firm_id': [1, 2, 3],
        'BusinessName': ['XYZ Corp', 'LMN Ltd', 'ABC Inc'],
        'Active': [True, False, True],
        'Address': ['123 Main St', '789 Oak St', '456 Elm St'],
        'Zip Code': ['12345', '67890', '54321']
    })

    # Create a sample newData DataFrame which is empty
    newData = pd.DataFrame({})

    # Call your function to find matching datapoints
    error_message = compare_dataframes_sos(historicalData, newData)

    # Check if the result is an empty DataFrame
    assert error_message is False


# Define a passing test case for update_dataframe_with_yellow_pages_data
# Define a passing test case for update_dataframe_with_yellow_pages_data
def test_update_dataframe_with_yellow_pages_data_fail():
    # Create a sample 'data' DataFrame with the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': [np.nan],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data'
    updated_data = update_dataframe_with_yellow_pages_data(data)

    # Check if the 'data' DataFrame has been updated correctly
    assert not updated_data


def test_update_dataframe_with_yellow_pages_data_pass():
    # Create a sample 'data' DataFrame with no matching 'BusinessName' and the specified columns
    data = pd.DataFrame({
        'Firm_id': [2],
        'BusinessName': ["Able Fence, Inc."],
        'BusinessNameCorrect': [False],
        'BusinessNameUpdate': [np.nan],
        'BusinessNameFound': [np.nan],
        'Address': ["blah"],
        'BusinessAddressCorrect': [False],
        'BusinessAddressUpdate': [np.nan],
        'BusinessAddressFound': [np.nan],
        'Zip Code': ["blah"],
        'BusinessZipCorrect': [False],
        'BusinessZipUpdate': [np.nan],
        'BusinessZipFound': [np.nan],
        'Website': ['blah'],
        'BusinessWebsiteCorrect': [False],
        'BusinessWebsiteUpdate': [np.nan],
        'BusinessWebsiteFound': [np.nan],
        'Phone': ['blah'],
        'BusinessPhoneCorrect': [False],
        'BusinessPhoneUpdate': [np.nan],
        'BusinessPhoneFound': [np.nan],
        'City': ["Saint Paul"]
    })

    # Apply the function to update 'data' with non-matching data
    updated_data = update_dataframe_with_yellow_pages_data(data)

    # Check that none of the rows in 'data' have been updated
    assert isinstance(updated_data, pd.DataFrame)

    expected_columns = [
        'Firm_id', 'BusinessName', 'BusinessNameCorrect', 'BusinessNameUpdate', "BusinessNameFound",
        'Address', 'BusinessAddressCorrect', 'BusinessAddressUpdate', 'BusinessAddressFound',
        'Zip Code', 'BusinessZipCorrect', 'BusinessZipUpdate', 'BusinessZipFound',
        'Website', 'BusinessWebsiteCorrect', 'BusinessWebsiteUpdate', 'BusinessWebsiteFound',
        'Phone', 'BusinessPhoneCorrect', 'BusinessPhoneUpdate', 'BusinessPhoneFound',
        'City'
    ]
    actual_columns = updated_data.columns.tolist()
    assert actual_columns == expected_columns

    assert not updated_data.empty
