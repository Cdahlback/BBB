import pandas as pd
import unittest 
from Rania import get_valid_businesses_info


class TestGetValidBusinessesInfo(unittest.TestCase):

    def setUp(self):
        self.file_name = r'C:\Users\Rania\Documents\GitHub\BBB\BBBDM\Data\mn_business.csv'
    
    def test_valid_businesses(self):
        # Test when there are valid businesses
        active_businesses_info = get_valid_businesses_info(self.file_name)
        self.assertIsInstance(active_businesses_info, pd.DataFrame)
        self.assertTrue(all(active_businesses_info['active'].str.strip().str.upper() == 'TRUE'))

    def test_invalid_file(self):
        # Test when the file does not exist or is invalid
        invalid_file_name = 'invalid_file.csv'
        with self.assertRaises(FileNotFoundError):
            get_valid_businesses_info(invalid_file_name)

    def test_inactive_businesses(self):
        # Test when there are no active businesses
        # Create a sample DataFrame with 'active' values as 'FALSE'
        data = {'name': ['Business1', 'Business2'], 'active': ['FALSE', 'FALSE']}
        df = pd.DataFrame(data)
        df.to_csv('inactive_businesses.csv', index=False)
        inactive_businesses_info = get_valid_businesses_info('inactive_businesses.csv')
        self.assertIsInstance(inactive_businesses_info, pd.DataFrame)
        self.assertTrue(inactive_businesses_info.empty)

    
    
   
if __name__ == '__main__':
    unittest.main()
