import pandas as pd
import pytest
import importlib.util
import numpy as np
from pathlib import Path
import os

modular = importlib.util.spec_from_file_location(
    "main", str(Path(__file__).parent.parent / "data_processing/main.py")
)

main = importlib.util.module_from_spec(modular)
modular.loader.exec_module(main)


# Define a test case for a passing case in compare_dataframes
def test_compare_dataframes_pass():
    # Create a sample historicalData DataFrame
    historicalData = pd.DataFrame(
        {
            "Firm_id": [1, 2, 3],
            "BusinessName": ["XYZ Corp", "LMN Ltd", "ABC Inc"],
            "Active": [True, False, True],
            "Address": ["123 Main St", "789 Oak St", "456 Elm St"],
            "Zip Code": ["12345", "67890", "54321"],
        }
    )

    # Create a sample newData DataFrame with matching and non-matching rows
    newData = pd.DataFrame(
        {
            "Business Name": ["XYZ Corp", "PQR Corp", "ABC Inc"],
            "Address 1": ["123 Main St", "777 Maple St", "456 Elm St"],
            "Zip Code": ["12345", "99999", "54321"],
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
    result_df = main.compare_dataframes(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Check if the result has the expected columns
    expected_columns = [
        "Firm_id",
        "BusinessName",
        "MatchesAddress",
        "Address_new",
        "MatchesZip",
        "Zip Code_new",
        "Business Filing Type",
        "Filing Date",
        "Status",
        "Address 2",
        "City",
        "Region Code",
        "Party Full Name",
        "Next Renewal Due Date",
    ]
    assert result_df.columns.tolist() == expected_columns


# Define a test case for a failing case in compare_dataframes
def test_compare_dataframes_fail():
    # Create two sample DataFrames with non-overlapping data
    historicalData = pd.DataFrame(
        {
            "Firm_id": [1, 2, 3],
            "BusinessName": ["XYZ Corp", "LMN Ltd", "ABC Inc"],
            "Active": [True, False, True],
            "Address": ["123 Main St", "789 Oak St", "456 Elm St"],
            "Zip Code": ["12345", "67890", "54321"],
        }
    )

    # Create a sample newData DataFrame which is empty
    newData = pd.DataFrame({})

    # Call your function to find matching datapoints
    error_message = main.compare_dataframes(historicalData, newData)

    # Check if the result is an empty DataFrame
    assert error_message == False


def test_join_dataframe_firmid():
    # create test dataframes
    df1 = pd.DataFrame(
        {
            "firm_id": [1, 2, 3],
            "state_incorporated": ["MN", "MN", "MN"],
            "name_id": [1, 2, 3],
            "company_name": ["ABC Inc.", "XYZ Corp.", "123 LLC"],
            "phone_id": [1, 2, 3],
            "phone": ["123-456-7890", "555-555-5555", "999-999-9999"],
        }
    )
    df2 = pd.DataFrame(
        {
            "firm_id": [2, 3, 4],
            "url_id": [1, 2, 3],
            "url": [
                "http://www.xyzcorp.com",
                "http://www.123llc.com",
                "http://www.456inc.com",
            ],
            "email_id": [1, 2, 3],
            "email": ["info@xyzcorp.com", "info@123llc.com", "info@456inc.com"],
        }
    )
    df3 = pd.DataFrame(
        {
            "firm_id": [1, 3, 4],
            "address_1": ["123 Main St", "456 Elm St", "789 Oak St"],
            "address_2": ["Suite 100", "Suite 200", ""],
            "city": ["Minneapolis", "St. Paul", "Bloomington"],
            "zip_code": ["55401", "55101", "55420"],
        }
    )

    # expected output
    expected_output = pd.DataFrame(
        {
            "firm_id": [1, 2, 3],
            "state_incorporated": ["MN", "MN", "MN"],
            "name_id": [1.0, 2.0, 3.0],
            "BusinessName": ["ABC Inc.", "XYZ Corp.", "123 LLC"],
            "phone_id": [1.0, 2.0, 3.0],
            "Phone": ["123-456-7890", "555-555-5555", "999-999-9999"],
            "url_id": [np.nan, 1.0, 2.0],
            "Website": [np.nan, "http://www.xyzcorp.com", "http://www.123llc.com"],
            "email_id": [np.nan, 1.0, 2.0],
            "Email": [np.nan, "info@xyzcorp.com", "info@123llc.com"],
            "address_1": ["123 Main St", np.nan, "456 Elm St"],
            "address_2": ["Suite 100", np.nan, "Suite 200"],
            "City": ["Minneapolis", np.nan, "St. Paul"],
            "zip_code": ["55401", np.nan, "55101"],
            "Address": [
                "123 Main St Suite 100 Minneapolis",
                np.nan,
                "456 Elm St Suite 200 St. Paul",
            ],
        }
    )

    # # test function with three dataframes
    # example_dataframe = main.join_dataframe_firmid(df1, df2, df3)

    # Iterate through each element in example_dataframe and check if it's equal to the expected output
    # for i in range(len(example_dataframe)):
    #     for j in range(len(example_dataframe.columns)):
    #         assert example_dataframe.iloc[i,j] == expected_output.iloc[i,j]

    actual = main.join_dataframe_firmid(df1, df2, df3)

    assert main.join_dataframe_firmid(df1, df2, df3).equals(expected_output)

    # test function with no dataframes
    assert main.join_dataframe_firmid() == False


test_join_dataframe_firmid()

# Test filtering of valid DataFrames
def test_filter_success():
    df = pd.DataFrame(
        {
            "name": ["Company A", "Company C"],
            "address": ["123 Main St", "456 Oak St"],
            "phone": ["5551234567", "5557891234"],
            "website": ["www.companya.com", "www.companyc.com"],
            "email": ["email@companya.com", "email@companyc.com"],
        }
    )

    valid_df, invalid_df = main.filter_dataframes(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 0

    assert all(
        col in valid_df.columns
        for col in ["name", "address", "phone", "website", "email"]
    )

    assert "Company A" in valid_df["name"].values
    assert "Company C" in valid_df["name"].values


# Test filtering of invalid DataFrames
def test_filter_failure():
    df = pd.DataFrame(
        {
            "name": ["", None],
            "address": ["", None],
            "phone": ["12345678901234567890", None],
            "website": ["", None],
            "email": ["", None],
        }
    )

    valid_df, invalid_df = main.filter_dataframes(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 2

    assert all(
        col in invalid_df.columns
        for col in ["name", "address", "phone", "website", "email"]
    )


# Test case for a successful scenario
def test_successful_scenario():
    # Create a sample CSV file with active and inactive businesses
    sample_data = {
        "business_name": ["Business A", "Business B"],
        "active": ["TRUE", "FALSE"],
    }
    # Create a pandas DataFrame from the sample data
    sample_df = pd.DataFrame(sample_data)
    # Define the filename for the sample CSV file
    sample_csv = "sample_businesses.csv"
    # Save the DataFrame as a CSV file
    sample_df.to_csv(sample_csv, index=False)

    # Call the function with the sample CSV file
    result = main.get_valid_businesses_info(sample_csv)

    # updated to remove the file after it's created
    os.remove(Path(__file__).parent / "sample_businesses.csv")
    # Assert that the result is not None and contains expected data
    assert result is not None
    assert len(result) == 1  # Only 'Business A' is active in the sample data


def test_normalize_email_success():
    """
    Test normalization of email addresses
    """
    data = {
        "Email": ["johndoe@example.com", "invalidemail", "alice.smith@gmail.com"],
        "Phone Number": ["123-456-7890", "invalid phone", "9876543210"],
        "Zipcode": ["12345", "ABCDE", "54321"],
    }
    data = pd.DataFrame(data)
    result = main.normalize_dataframe(data)
    assert result.loc[0, "Email"] == "johndoe@example.com"
    assert result.loc[1, "Email"] is None  # Invalid email
    assert result.loc[2, "Email"] == "alice.smith@gmail.com"


def test_normalize_phone_number_success():
    data = {
        "Email": ["johndoe@example.com", "invalidemail", "alice.smith@gmail.com"],
        "Phone Number": ["123-456-7890", "invalid phone", "9876543210"],
        "Zipcode": ["12345", "ABCDE", "54321"],
    }
    data = pd.DataFrame(data)
    result = main.normalize_dataframe(data)
    assert result.loc[0, "Phone Number"] == "1234567890"
    assert result.loc[1, "Phone Number"] is None  # Invalid phone number
    assert result.loc[2, "Phone Number"] == "9876543210"
