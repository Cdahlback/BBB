import numpy as np
import pandas as pd
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from BBBDM.lib.data_processing import (
    address_match_found,
    filter_dataframes,
    get_valid_businesses_info,
    join_dataframe_firmid,
)



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

    valid_df, invalid_df = filter_dataframes(df)

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

    valid_df, invalid_df = filter_dataframes(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 2

    assert all(
        col in invalid_df.columns
        for col in ["name", "address", "phone", "website", "email"]
    )


def test_matching_address_with_same_address():
    # Test case 1: Identical addresses, expecting match_found = 1
    historical_addresses = [
        "123 Main St, Springfield",
        "456 Pine St, Boston",
        "789 Oak St, Los Angeles",
    ]
    new_addresses = [
        "123 Main St, Springfield",
        "456 Pine St, Boston",
        "789 Oak St, Los Angeles",
    ]
    expected_output = pd.DataFrame(
        {
            "historical_address": historical_addresses,
            "found_address": new_addresses,
            "match_found": [1, 1, 1],
            "city_match_name": ["N/A", "N/A", "N/A"],
        }
    )
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)


def test_matching_address_with_different_address_same_cities():
    # Test case 2: Addresses with matching cities, expecting match_found = 2
    historical_addresses = [
        "124 Main St, Springfield",
        "456 Pine St, Boston",
        "789 Oak St, Los Angeles",
    ]
    new_addresses = [
        "123 Main St, Springfield",
        "456 Maple St, Boston",
        "111 Oak St, Los Angeles",
    ]
    expected_output = pd.DataFrame(
        {
            "historical_address": historical_addresses,
            "found_address": new_addresses,
            "match_found": [2, 2, 2],
            "city_match_name": ["Springfield", "Boston", "Los Angeles"],
        }
    )
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)


def test_matching_address_with_different_address_different_cities():
    # Test case 3: No matching addresses, expecting match_found = 0
    historical_addresses = [
        "123 Main St, Springfield",
        "456 Pine St, Boston",
        "789 Oak St, Los Angeles",
    ]
    new_addresses = [
        "456 Maple St, California",
        "789 Oak St, California",
        "555 Elm St, Chicago",
    ]
    expected_output = pd.DataFrame(
        {
            "historical_address": historical_addresses,
            "found_address": new_addresses,
            "match_found": [0, 0, 0],
            "city_match_name": ["N/A", "N/A", "N/A"],
        }
    )
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)


def test_matching_address_with_mixed_examples():
    historical_addresses = [
        "123 Main St, Springfield",
        "456 Pine St, Boston",
        "1340 Warren St, Mankato",
    ]
    new_addresses = [
        "123 Main St, Springfield",
        "789 Oak St, California",
        "200 Briargate Rd, Mankato",
    ]
    expected_output = pd.DataFrame(
        {
            "historical_address": historical_addresses,
            "found_address": new_addresses,
            "match_found": [1, 0, 2],
            "city_match_name": ["N/A", "N/A", "Mankato"],
        }
    )
    actual_output  = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)


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
            "state_incorporated": [["MN"], ["MN"], ["MN"]],
            "name_id": [[1.0], [2.0], [3.0]],
            "BusinessName": [["ABC Inc."], ["XYZ Corp."], ["123 LLC"]],
            "phone_id": [[1.0], [2.0], [3.0]],
            "Phone": [["123-456-7890"], ["555-555-5555"], ["999-999-9999"]],
            "url_id": [[np.nan], [1.0], [2.0]],
            "Website": [[np.nan], ["http://www.xyzcorp.com"], ["http://www.123llc.com"]],
            "email_id": [[np.nan], [1.0], [2.0]],
            "Email": [[np.nan], ["info@xyzcorp.com"], ["info@123llc.com"]],
            "address_1": [["123 Main St"], [np.nan], ["456 Elm St"]],
            "address_2": [["Suite 100"], [np.nan], ["Suite 200"]],
            "City": [["Minneapolis"], [np.nan], ["St. Paul"]],
            "zip_code": [["55401"], [np.nan], ["55101"]],
            "Address": [
                ["123 Main St Suite 100 Minneapolis"],
                [np.nan],
                ["456 Elm St Suite 200 St. Paul"],
            ],
        }
    )

    #Resulting DataFrame
    result = join_dataframe_firmid(df1, df2, df3)

    assert result.equals(expected_output)

    # test function with no dataframes
    assert join_dataframe_firmid() == False





''''
# Test case for a successful scenario
def test_all_businesses_active():
    # Create a sample CSV file with active and inactive businesses
    sample_data = {'business_name': ['Business A', 'Business B'],
                    'active': ['True', 'TRUE']}  # Both in uppercase 'True'
    # Create a pandas DataFrame from the sample data
    sample_df = pd.DataFrame(sample_data)
    # Define the filename for the sample CSV file
    sample_csv = 'sample_businesses.csv'
    # Save the DataFrame as a CSV file
    sample_df.to_csv(sample_csv, index=False)

    # Call the function with the sample CSV file
    actual_output = get_valid_businesses_info(sample_csv)
   
    # Define the expected DataFrame with 'True' for 'active'
    expected_data = {'business_name': ['Business A','Business B'],
                     'active': ['TRUE','TRUE']} 
    expected_output = pd.DataFrame(expected_data)
    
    # Assert that the result is not None and contains expected data
    assert expected_output.equals(actual_output)
    
# Test case for when there are no active businesses
def test_no_active_businesses():
    # Create a sample CSV file with no active businesses
    sample_data = {'business_name': [],  # Empty list means no active businesses
                    'active': []}  # Empty list means no active businesses
    # Create a pandas DataFrame from the sample data
    sample_df = pd.DataFrame(sample_data)
    # Define the filename for the sample CSV file
    sample_csv = 'sample_businesses.csv'
    # Save the DataFrame as a CSV file
    sample_df.to_csv(sample_csv, index=False)

    # Call the function with the sample CSV file
    actual_output = get_valid_businesses_info(sample_csv)
    

    # Define the expected DataFrame for no active businesses with explicit data type
    expected_data = {'business_name': [], 'active': []}
    expected_output = pd.DataFrame(expected_data, dtype='object')
   

    # Assert that the result is equal to the expected output using pd.testing.assert_frame_equal
    pd.testing.assert_frame_equal(expected_output, actual_output)


# Test case for a mix of active and non-active businesses
def test_active_and_non_active_businesses():
    # Create a sample CSV file with active and non-active businesses
    sample_data = {'business_name': ['Business A', 'Business B', 'Business C'],
                   'active': ['TRUE', 'TrUE', 'FALSE']}  # Mix of active and non-active businesses
    # Create a pandas DataFrame from the sample data
    sample_df = pd.DataFrame(sample_data)
    # Define the filename for the sample CSV file
    sample_csv = 'sample_businesses.csv'
    # Save the DataFrame as a CSV file
    sample_df.to_csv(sample_csv, index=False)
    actual_output = get_valid_businesses_info(sample_csv)
    
    expected_data={'business_name': ['Business A','Business B'],
                     'active': ['TRUE','TRUE']}
    expected_output=pd.DataFrame(expected_data, dtype='object')
    # Assert that the result is equal to the expected output using pd.testing.assert_frame_equal
    pd.testing.assert_frame_equal(expected_output, actual_output)
'''
