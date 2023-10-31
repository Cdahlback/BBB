import unittest

import pandas as pd
from BBBDM.data_processing.main import normalize_address

from Lib.Normalizing import normalize_dataframe, normalize_email, normalize_url, normalize_us_phone_number, standardizeName


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
def test_normalize_us_phone_number():
    """Test the phone number normalization function."""
    test_cases = [
        ("202-555-0113", "+1 202-555-0113"),
        ("15551234567", "+1 555-123-4567"),
        ("5551234567", "+1 555-123-4567"),
        ("555123456", None),
        ("212555123456", None),
        ("25551234a567", None)
    ]
    for phone_str, expected in test_cases:
        try:
            normalized = normalize_us_phone_number(phone_str)
            assert normalized == expected, f"Expected {expected} but got {normalized} for input {phone_str}"
        except ValueError as e:
            assert expected is None, f"Unexpected exception for {phone_str}: {e}"

def test_standardizeName():
    """Test the business name standardization function."""
    test_cases = [
        ("Example & Co.", "example and co"),
        ("McDonald's", "mcdonalds"),
        ("   Spaces  & Tabs    ", "spaces and tabs"),
        ("OnlyAlphabets", "onlyalphabets")
    ]
    for name, expected in test_cases:
        result = standardizeName(name)
        assert result == expected, f"Expected {expected} but got {result} for input {name}"

def test_normalize_address():
    """Test the address normalization function."""
    test_cases = [
        ({
            'country_area': 'CA',
            'city': 'Mountain View',
            'country_code':'US',
            'postal_code': '94041',
            'street_address': '123 Main St'
        }, {
            'country_area': 'CA',
            'city': 'MOUNTAIN VIEW',
            'country_code':'US',
            'postal_code': '94041',
            'street_address': '123 Main St',
            'city_area': '',
            'sorting_code': ''
        }),
    ]
    for addr, expected in test_cases:
        result = normalize_address(addr)
        assert result == expected, f"Expected {expected} but got {result} for input {addr}"

def test_normalize_url():
    """Test the URL normalization function."""
    test_cases = [
        ("www.Example.com", "http://www.example.com"),
        ("http://www.example.com", "http://www.example.com"),
        ("https://Example.COM", "https://example.com"),
        ("NoProtocol.com", "http://noprotocol.com")
    ]
    for url, expected in test_cases:
        result = normalize_url(url)
        assert result == expected, f"Expected {expected} but got {result} for input {url}"

if __name__ == "__main__":
    # Run the test functions
    test_normalize_us_phone_number()
    test_standardizeName()
    test_normalize_address()
    test_normalize_url()


def test_normalize_with_invalid_emails():
    emails_invalid = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    expected_output = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_invalid)
    assert expected_output.equals(actual_output)

def test_normalize_with_valid_emails():
    emails_valid = pd.DataFrame({'email': ['W3071442@aol.com','Anjorinr1@student.iugb.edu.ci','Raniaanjor@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','anjorinr1@student.iugb.edu.ci','raniaanjor@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_valid)
    assert expected_output.equals(actual_output)

def test_normalize_with_mixed_emails():
    emails_mixed = pd.DataFrame({'email': [' W3071442@aol.com ','raniaanjor#gmail.com','Anjorinr1@student.iugb.edu.ci','@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','raniaanjor#gmail.com','anjorinr1@student.iugb.edu.ci','@gmail.com']})
    actual_output = normalize_email.normalize_dataframe(emails_mixed)
    assert expected_output.equals(actual_output)