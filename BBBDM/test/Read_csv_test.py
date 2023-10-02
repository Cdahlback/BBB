import unittest
import pandas as pd

import sys
sys.path.append(r'C:\Users\Rania\Documents\GitHub\BBB')

# Import your function to be tested
from BBBDM.data_processing.Rania import get_valid_businesses_info  

class TestGetValidBusinessesInfo(unittest.TestCase):

    # Test case for a successful scenario
    def test_successful_scenario(self):
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
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)  # Only 'Business A' is active in the sample data

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