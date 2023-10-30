import unittest

import pandas as pd

from Lib.Normalizing import get_valid_businesses_info
from Lib.data_processing import address_match_found, filter_dataframes, join_dataframe_firmid



class TestGetValidBusinessesInfo(unittest.TestCase):

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
        result = get_valid_businesses_info(sample_csv)

        # Assert that the result is not None and contains expected data
        assert result is not None
        assert len(result) == 1 # Only 'Business A' is active in the sample data

    # Test case for a failure scenario
    def test_failure_scenario(self):
        # Call the function with a non-existent file
        non_existent_file = 'non_existent_file.csv'
        result = get_valid_businesses_info(non_existent_file)

        # Assert that the result is None (indicating an error occurred)
        self.assertIsNone(result)

    # Test case for all "active" values as 'FALSE'
    def test_all_inactive(self):
        # Create a sample CSV file with all inactive businesses
        sample_data = {'business_name': ['Business C', 'Business D'],
                       'active': ['FALSE', 'FALSE']}
        sample_df = pd.DataFrame(sample_data)
        sample_csv = 'sample_all_inactive.csv'
        sample_df.to_csv(sample_csv, index=False)

        # Call the function with the sample CSV file
        result = get_valid_businesses_info(sample_csv)

        # Assert that the result is not None and contains expected data
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)  # All businesses are inactive in this scenario

if __name__ == '__main__':
    unittest.main()

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
    actual = join_dataframe_firmid(df1, df2, df3)

    # Compare
    assert actual.equals(expected)

def test_join_dataframe_firmid_failed():
    "Test what would happen if the FirmID failed"
    # Input dataframes
    df1 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Name': ['A', 'B', 'C']})
    df2 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Business_type': ['Construction', 'Construction', 'Something']})
    df3 = pd.DataFrame({'FirmIDD': [1, 2, 3], 'Location': ['USA', 'USA', 'USA']})

    #Expected output
    expected = False

    # Actual output
    actual = join_dataframe_firmid(df1, df2, df3)

    # Compare
    assert actual == expected

def test_filter_success():
    df = pd.DataFrame({
        'name': ['Company A', 'Company C'],
        'address': ['123 Main St', '456 Oak St'],
        'phone': ['5551234567', '5557891234'],
        'website': ['www.companya.com', 'www.companyc.com'],
        'email': ['email@companya.com', 'email@companyc.com']
    })

    valid_df, invalid_df = filter_dataframes(df)

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

    valid_df, invalid_df = filter_dataframes(df)

    assert len(valid_df) == 0
    assert len(invalid_df) == 2

    assert all(col in invalid_df.columns for col in ['name', 'address', 'phone', 'website', 'email'])

if __name__ == "__main__":
    test_filter_success()
    test_filter_failure()
def test_matching_address_with_same_address():
    # Test case 1: Identical addresses, expecting match_found = 1
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [1, 1, 1],'city_match_name':['N/A','N/A','N/A']})
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_different_address_same_cities():
    # Test case 2: Addresses with matching cities, expecting match_found = 2
    historical_addresses = ['124 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['123 Main St, Springfield', '456 Maple St, Boston', '111 Oak St, Los Angeles']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [2, 2, 2],'city_match_name':['Springfield','Boston','Los Angeles']})
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)
def test_matching_address_with_different_address_different_cities():
    # Test case 3: No matching addresses, expecting match_found = 0
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '789 Oak St, Los Angeles']
    new_addresses = ['456 Maple St, California', '789 Oak St, California', '555 Elm St, Chicago']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [0, 0, 0],'city_match_name':['N/A','N/A','N/A']})
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)

def test_matching_address_with_mixed_examples():
    historical_addresses = ['123 Main St, Springfield', '456 Pine St, Boston', '1340 Warren St, Mankato']
    new_addresses = ['123 Main St, Springfield', '789 Oak St, California', '200 Briargate Rd, Mankato']
    expected_output = pd.DataFrame({'historical_address': historical_addresses, 'found_address': new_addresses, 'match_found': [1, 0, 2],'city_match_name':['N/A','N/A','Mankato']})
    actual_output = address_match_found(historical_addresses, new_addresses)
    assert expected_output.equals(actual_output)    

