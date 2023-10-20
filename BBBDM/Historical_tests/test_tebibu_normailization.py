import sys
import logging

# Add the project path to the system path
sys.path.append(r'C:\Users\tebib\OneDrive\Desktop\Project 1\BBB')

# Import normalization functions from the module
from BBBDM.data_processing.Tebibu_Normalization import (
    normalize_us_phone_number, standardizeName,
    normalize_address_i18n as normalize_address, 
    normalize_url
)

# Logging setup
logging.basicConfig(filename='normalization.log', level=logging.INFO)

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
