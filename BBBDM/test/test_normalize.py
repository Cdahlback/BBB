import unittest

import pandas as pd

from BBBDM.lib.Normalizing import (
    normalize_address,
    normalize_dataframe,
    normalize_url,
    normalize_zipcode,
    normalize_us_phone_number,
    standardizeName,
)

# TODO: Need to make tests for normalize_email function


def test_zipcodes():
    zipcode=["55001","55  111","ABCD"]
    expected_output= pd.DataFrame({
                'Original Zip Code': ["55001","55  111","ABCD"],
                'Standardized Zip Code': ["55001", "55111", "N/A"]
            })
    print(expected_output)
    
    actual_output=normalize_zipcode(zipcode)
    print(actual_output)
    assert expected_output.equals(actual_output)




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


def test_normalize_with_invalid_emails():
    emails_invalid = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    expected_output = pd.DataFrame({'email': ['raniaanjor#gmail.com', 'Rania@.com', '@gmail.com']})
    actual_output = normalize_dataframe(emails_invalid)
    assert expected_output.equals(actual_output)

def test_normalize_with_valid_emails():
    emails_valid = pd.DataFrame({'email': ['W3071442@aol.com','Anjorinr1@student.iugb.edu.ci','Raniaanjor@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','anjorinr1@student.iugb.edu.ci','raniaanjor@gmail.com']})
    actual_output = normalize_dataframe(emails_valid)
    assert expected_output.equals(actual_output)

def test_normalize_with_mixed_emails():
    emails_mixed = pd.DataFrame({'email': [' W3071442@aol.com ','raniaanjor#gmail.com','Anjorinr1@student.iugb.edu.ci','@gmail.com']})
    expected_output = pd.DataFrame({'email': ['w3071442@aol.com','raniaanjor#gmail.com','anjorinr1@student.iugb.edu.ci','@gmail.com']})
    actual_output = normalize_dataframe(emails_mixed)
    assert expected_output.equals(actual_output)