import unittest
from unittest.mock import MagicMock, patch

from Extract_Data.create_urls import build_url_from_email, extract_domain_name

"""File used to test creation of urls, creation from emails and also web searches"""


class TestCreateURLs(unittest.TestCase):
    def test_valid_email(self):
        email = "john.doe@example.com"
        expected_url = "https://www.example.com/"

        result = build_url_from_email(email)

        self.assertEqual(result, expected_url)

    def test_invalid_email(self):
        email = "not_an_email"
        expected_result = None

        result = build_url_from_email(email)

        self.assertEqual(result, expected_result)

    @patch("builtins.re")
    def test_clean_email_called(self, mock_re):
        email = "john.doe@example.com"
        mock_re.fullmatch.return_value = True
        mock_cleanEmail = MagicMock()
        with patch("__main__.cleanEmail", mock_cleanEmail):
            build_url_from_email(email)
            mock_cleanEmail.assert_called_once_with(email)

    @patch("__main__.bad_domain_names", ["example.com"])
    def test_bad_domain_name(self):
        email = "john.doe@example.com"
        expected_result = None

        result = build_url_from_email(email)

        self.assertEqual(result, expected_result)

    def test_extract_domain_name(self):
        url = "https://www.example.com"
        expected_result = "example.com"
        self.assertEqual(extract_domain_name(url), expected_result)

        url = "https://www.yelp.com"
        self.assertIsNone(extract_domain_name(url))

        url = "https://example.com"
        expected_result = "example.com"
        self.assertEqual(extract_domain_name(url), expected_result)

        url = "https://www.blog.example.com"
        expected_result = "example.com"
        self.assertEqual(extract_domain_name(url), expected_result)

        url = "https://www.example.com:8080"
        expected_result = "example.com"
        self.assertEqual(extract_domain_name(url), expected_result)

        url = "this is not a valid url"
        self.assertIsNone(extract_domain_name(url))
