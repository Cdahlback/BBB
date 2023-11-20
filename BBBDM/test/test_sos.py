import numpy as np
import pandas as pd
import pytest

from BBBDM.lib.sos_tools import compare_dataframes_sos


def test_compare_dataframes_pass1():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame(
        {
            "Firm_id": [1, 2, 3],
            "BusinessName": [["XYZ Corp"], ["LMN Ltd"], ["ABC Inc"]],
            "Active": [True, True, True],
            "Address": [["123 Main St"], ["789 Oak St"], ["456 Elm St"]],
            "Zip Code": [["12345"], ["67890"], ["54321"]],
            "Email": [["cdahlback@gmail.com"], ["cdahlback@yahoo.com"], ["cdahlback@hotmail.com"]]
        }
    )

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame(
        {
            "Business Name": ["XYZ Corp", "PQR Corp", "ABC Inc"],
            "Address 1": ["123 Main St", "777 Maple St", "456 Elm St"],
            "Zip Code New": ["12345", "99999", "54321"],
            "Business Filing Type": ["Type A", "Type B", "Type C"],
            "Filing Date": ["2022-01-01", "2022-02-02", "2022-03-03"],
            "Status": ["Active", "Inactive", "Active"],
            "Address 2": ["Suite 100", "", "Apt 2B"],
            "City": ["City1", "City2", "City3"],
            "Region Code": ["NY", "CA", "TX"],
            "Party Full Name": ["John Doe", "Jane Smith", "Bob Johnson"],
            "Next Renewal Due Date": ["2023-01-01", "2023-02-02", "2023-03-03"],
        }
    )

    # Call your function to find matching datapoints
    result_df = compare_dataframes_sos(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)


def test_compare_dataframes_pass2():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame(
        {
            "Firm_id": [1, 2, 3],
            "BusinessName": [["XYZ Corp"], ["LMN Ltd"], ["ABC Inc"]],
            "Active": [True, False, True],
            "Address": [["123 Main St"], ["789 Oak St"], ["456 Elm St"]],
            "Zip Code": [["12345"], ["67890"], ["54321"]],
        }
    )

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame(
        {
            "Business Name": ["XYZ Corp", "PQR Corp", "ABC Inc"],
            "Address 1": ["123 Main St", "777 Maple St", "456 Elm St"],
            "Zip Code New": ["12345", "99999", "54321"],
            "Business Filing Type": ["Type A", "Type B", "Type C"],
            "Filing Date": ["2022-01-01", "2022-02-02", "2022-03-03"],
            "Status": ["Active", "Inactive", "Active"],
            "Address 2": ["Suite 100", "", "Apt 2B"],
            "City": ["City1", "City2", "City3"],
            "Region Code": ["NY", "CA", "TX"],
            "Party Full Name": ["John Doe", "Jane Smith", "Bob Johnson"],
            "Next Renewal Due Date": ["2023-01-01", "2023-02-02", "2023-03-03"],
        }
    )

    # Call your function to find matching datapoints
    result_df = compare_dataframes_sos(historicalData, newData)

    # Check if the result has the expected columns
    expected_columns = [
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
        "BusinessZipFound",
    ]

    assert result_df.columns.tolist() == expected_columns


# Define a test case for a failing case in compare_dataframes
def test_compare_dataframes_fail():
    # Create two sample DataFrames with non-overlapping data
    historicalData = pd.DataFrame(
        {
            "Firm_id": [1, 2, 3],
            "BusinessName": [["XYZ Corp"], ["LMN Ltd"], ["ABC Inc"]],
            "Active": [True, False, True],
            "Address": [["123 Main St"], ["789 Oak St"], ["456 Elm St"]],
            "Zip Code": [["12345"], ["67890"], ["54321"]],
        }
    )

    # Create a sample newData DataFrame which is empty
    newData = pd.DataFrame({})

    # Use pytest.raises to check if compare_dataframes_sos raises ValueError
    with pytest.raises(ValueError):
        compare_dataframes_sos(historicalData, newData)

