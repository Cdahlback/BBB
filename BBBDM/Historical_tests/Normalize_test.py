import unittest
import pandas as pd
import re
import sys
sys.path.append(r'C:\Users\Rania\Documents\GitHub\BBB')

from BBBDM.historical_functions.Normalize import normalize_dataframe




class TestNormalizationFunctions(unittest.TestCase):

    def setUp(self):
        # Sample dataframe for testing
        data = {'Email': ['johndoe@example.com', 'invalidemail', 'alice.smith@gmail.com'],
                'Phone Number': ['123-456-7890', 'invalid phone', '9876543210'],
                'Zipcode': ['12345', 'ABCDE', '54321']}
        self.df = pd.DataFrame(data)

    def test_normalize_email_success(self):
        result = normalize_dataframe(self.df)
        self.assertEqual(result.loc[0, 'Email'], 'johndoe@example.com')
        self.assertIsNone(result.loc[1, 'Email'])  # Invalid email
        self.assertEqual(result.loc[2, 'Email'], 'alice.smith@gmail.com')

    def test_normalize_phone_number_success(self):
        result = normalize_dataframe(self.df)
        self.assertEqual(result.loc[0, 'Phone Number'], '1234567890')
        self.assertIsNone(result.loc[1, 'Phone Number'])  # Invalid phone number
        self.assertEqual(result.loc[2, 'Phone Number'], '9876543210')

    def test_normalize_zipcode_success(self):
        result = normalize_dataframe(self.df)
        self.assertEqual(result.loc[0, 'Zipcode'], '12345')
        self.assertIsNone(result.loc[1, 'Zipcode'])  # Invalid zipcode
        self.assertEqual(result.loc[2, 'Zipcode'], '54321')

if __name__ == '__main__':
    unittest.main()