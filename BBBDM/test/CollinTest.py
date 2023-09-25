import pandas as pd
import pytest
from BBBDM.data_processing.Collin import compare_dataframes  # Import your actual function here


# Define a test case for a passing case in find_matches
def test_find_matches_pass():
    # Create a sample historicalData dataframe
    historicalData = pd.DataFrame({
        'PrimaryKey': [None, 2, 3],
        'BusinessName': [None, 'XYZ Corp', 'LMN Ltd'],
        'Email': ['abc@example.com', 'xyz@example.com', 'lmn@example.com'],
        'Phone': ['123-456-7890', '987-654-3210', '555-555-5555'],
        'Address': ['123 Main St', '456 Elm St', '789 Oak St'],
        'Website': ['www.abc.com', 'www.xyz.com', 'www.lmn.com']
    })

    # Create a sample newData dataframe with some matching and non-matching rows
    newData = pd.DataFrame({
        'PrimaryKey': [None, 5, 6],
        'BusinessName': [None, 'XYZ Corporation', 'PQR Corp'],
        'Email': ['abc@example.com', 'newxyz@example.com', 'pqr@example.com'],
        'Phone': ['123-456-7890', '987-654-3210', '111-222-3333'],
        'Address': ['123 Main St', '456 Elm St', '777 Maple St'],
        'Website': ['www.abc.com', 'www.newxyz.com', 'www.pqr.com']
    })

    # Call your function to find matching datapoints
    result_df = compare_dataframes(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Check if the result has the expected columns
    expected_columns = ['PrimaryKey', 'BusinessNameMatch', 'EmailMatch', 'PhoneMatch', 'AddressMatch', 'WebsiteMatch']
    assert result_df.columns.tolist() == expected_columns


# Define a test case for a failing case in find_matches
def test_find_matches_fail():
    # Create two sample dataframes with non-overlapping data
    historicalData = pd.DataFrame({
        'PrimaryKey': [1, 2, 3],
        'BusinessName': ['ABC Inc', 'XYZ Corp', 'LMN Ltd'],
        'Email': ['abc@example.com', 'xyz@example.com', 'lmn@example.com'],
        'Phone': ['123-456-7890', '987-654-3210', '555-555-5555'],
        'Address': ['123 Main St', '456 Elm St', '789 Oak St'],
        'Website': ['www.abc.com', 'www.xyz.com', 'www.lmn.com']
    })
    # Create a sample newData dataframe which is empty
    newData = pd.DataFrame({})

    # Call your function to find matching datapoints
    result_df = compare_dataframes(historicalData, newData)

    # Check if the result is an empty DataFrame
    assert result_df.empty
