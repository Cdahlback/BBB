import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup
from Extract_Data.fill_ind_var_columns import get_html

"""File used to test getting the html from a website using bs4"""


class TestGetHtml(unittest.TestCase):
    @patch("requests.get")
    def test_get_html_valid_website(self, mock_get):
        # Mock response object
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.content = "<html><body></body></html>"

        mock_get.return_value = response_mock

        # Test with valid website
        website = "http://example.com"
        html = get_html(website)

        mock_get.assert_called_once_with(website, timeout=7)
        self.assertIsInstance(html, BeautifulSoup)

    @patch("requests.get")
    def test_get_html_invalid_website(self, mock_get):
        # Mock response object
        response_mock = MagicMock()
        response_mock.status_code = 404

        mock_get.return_value = response_mock

        # Test with invalid website
        website = "http://example.com/not-found"
        html = get_html(website)

        mock_get.assert_called_once_with(website, timeout=7)
        self.assertIsNone(html)

    def test_get_html_none_input(self):
        # Test with None input
        website = None
        html = get_html(website)

        self.assertIsNone(html)
