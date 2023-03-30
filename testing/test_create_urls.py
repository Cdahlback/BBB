import unittest
from unittest.mock import MagicMock, patch

from Extract_Data.create_urls import build_url_from_email


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