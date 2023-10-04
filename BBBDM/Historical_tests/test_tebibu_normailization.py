import unittest
import re
import sys
sys.path.append(r'C:\Users\tebib\OneDrive\Desktop\Project 1\BBB')


from BBBDM.historical_functions.Tebibu_Normalization import standardizeName, normalize_address, normalize_url

class TestNormalization(unittest.TestCase):
    def test_standardizeName(self):
        # Test cases for business name normalization
        self.assertEqual(standardizeName("Example & Co."), "example and co")
        self.assertEqual(standardizeName("Company-Name"), "company-name")
        self.assertEqual(standardizeName("ABC & XYZ"), "abc and xyz")
        
    def test_normalize_address(self):
        # Test cases for address normalization
        valid_address = "123 Main St Apt 456"
        self.assertEqual(normalize_address(valid_address), valid_address)
        
        invalid_address = "Invalid Address"
        self.assertIsNone(normalize_address(invalid_address))
        
    def test_normalize_url(self):
        # Test cases for URL normalization
        self.assertEqual(normalize_url("www.example.com"), "http://www.example.com")
        self.assertEqual(normalize_url("https://www.example.com"), "https://www.example.com")
        self.assertEqual(normalize_url("www.example.com/path"), "http://www.example.com/path")
        
if __name__ == '__main__':
    unittest.main()
