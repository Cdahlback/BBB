import pandas as pd
import pytest
import importlib.util
from pathlib import Path
import os

modular = importlib.util.spec_from_file_location("chris_function", str(Path(__file__).parent.parent / 'data_processing/main.py'))

main = importlib.util.module_from_spec(modular)
modular.loader.exec_module(main)



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
        'Zip Code': ['12345', '99999', '54321'],
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
    result_df = main.compare_dataframes(historicalData, newData)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame)

    # Check if the result has the expected columns
    expected_columns = ['Firm_id', 'BusinessName', 'MatchesAddress', 'Address_new', 'MatchesZip', 'Zip Code_new',
                        'Business Filing Type', 'Filing Date', 'Status', 'Address 2', 'City', 'Region Code',
                        'Party Full Name', 'Next Renewal Due Date']
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
    error_message = main.compare_dataframes(historicalData, newData)

    # Check if the result is an empty DataFrame
    assert error_message == False


# Define a test case for a passing case in compare_dataframes
def test_join_dataframe_firmid_multiple_success():
    """
    Test joining multiple dataframes in the given function
    """
    # Input dataframes
    df1 = pd.DataFrame({'FirmID': [1, 2, 3], 'Name': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'FirmID': [1, 2, 3], 'Business_type': ['Construction', 'Construction', 'Something']})
    df3 = pd.DataFrame({'FirmID': [1, 2, 3], 'Location': ['USA', 'USA', 'USA']})

    #Expected output
    expected = pd.DataFrame({'FirmID': [1, 2, 3], 'Name': ['A', 'B', 'C'], 'Business_type': ['Construction', 'Construction', 'Something'], 'Location': ['USA', 'USA', 'USA']})

    # Actual output
    actual = main.join_dataframe_firmid(df1, df2, df3)

    # Compare
    assert actual.equals(expected)


# Define a test case for a failing case in compare_dataframes
def test_join_dataframe_firmid_failed():
    "Test what would happen if the FirmID failed"
    # Input dataframes
    df1 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Name': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Business_type': ['Construction', 'Construction', 'Something']})
    df3 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Location': ['USA', 'USA', 'USA']})

    #Expected output
    expected = False

    # Actual output
    actual = main.join_dataframe_firmid(df1, df2, df3)

    # Compare
    assert actual == expected


# Test filtering of valid DataFrames
def test_filter_success():
    df = pd.DataFrame({
        'name': ['Company A', 'Company C'],
        'address': ['123 Main St', '456 Oak St'],
        'phone': ['5551234567', '5557891234'],
        'website': ['www.companya.com', 'www.companyc.com'],
        'email': ['email@companya.com', 'email@companyc.com']
    })

    valid_df, invalid_df = main.filter_dataframes(df)

    assert len(valid_df) == 2
    assert len(invalid_df) == 0

    assert all(col in valid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])

    assert 'Company A' in valid_df['name'].values
    assert 'Company C' in valid_df['name'].values

# Test filtering of invalid DataFrames
def test_filter_failure():
    df = pd.DataFrame({
        'name': ['', None],
        'address': ['', None],
        'phone': ['12345678901234567890', None],
        'website': ['', None],
        'email': ['', None]
    })

    valid_df, invalid_df = main.filter_dataframes(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 2

    assert all(col in invalid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])


# Test case for a successful scenario
def test_successful_scenario():
    # Create a sample CSV file with active and inactive businesses
    sample_data = {'business_name': ['Business A', 'Business B'],
                    'active': ['TRUE', 'FALSE']}
    # Create a pandas DataFrame from the sample data
    sample_df = pd.DataFrame(sample_data)
        # Define the filename for the sample CSV file
    sample_csv = 'sample_businesses.csv'
    # Save the DataFrame as a CSV file 
    sample_df.to_csv(sample_csv, index=False)

    # Call the function with the sample CSV file
    result = main.get_valid_businesses_info(sample_csv)

    #updated to remove the file after it's created
    os.remove(Path(__file__).parent / 'sample_businesses.csv')
    # Assert that the result is not None and contains expected data
    assert result is not None
    assert len(result) == 1 # Only 'Business A' is active in the sample data


def test_normalize_email_success():
    """
    Test normalization of email addresses
    """
    data = {'Email': ['johndoe@example.com', 'invalidemail', 'alice.smith@gmail.com'],
            'Phone Number': ['123-456-7890', 'invalid phone', '9876543210'],
            'Zipcode': ['12345', 'ABCDE', '54321']}
    data = pd.DataFrame(data)
    result = main.normalize_dataframe(data)
    assert result.loc[0, 'Email'] == 'johndoe@example.com'
    assert result.loc[1, 'Email'] is None  # Invalid email
    assert result.loc[2, 'Email'] == 'alice.smith@gmail.com'


def test_normalize_phone_number_success():
    data = {'Email': ['johndoe@example.com', 'invalidemail', 'alice.smith@gmail.com'],
            'Phone Number': ['123-456-7890', 'invalid phone', '9876543210'],
            'Zipcode': ['12345', 'ABCDE', '54321']}
    data = pd.DataFrame(data)
    result = main.normalize_dataframe(data)
    assert result.loc[0, 'Phone Number'] == '1234567890'
    assert result.loc[1, 'Phone Number'] is None  # Invalid phone number
    assert result.loc[2, 'Phone Number'] == '9876543210'


    