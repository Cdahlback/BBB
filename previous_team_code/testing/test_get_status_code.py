import unittest
from unittest.mock import patch

import requests
from Not_Our_Code.get_status_codes import status_code

"""File used to test our function which gets status codes for a website"""


class TestStatusCode(unittest.TestCase):
    def setUp(self):
        self.url = "http://www.example.com"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.timeout = 5

    @patch("Not_Our_Code.get_status_codes.requests.get")
    def test_status_code_success(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertEqual(status_code(self.url, self.headers, self.timeout), 200)

    @patch("Not_Our_Code.get_status_codes.requests.get")
    def test_status_code_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)

    @patch("Not_Our_Code.get_status_codes.requests.get")
    def test_status_code_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)

    @patch("Not_Our_Code.get_status_codes.requests.get")
    def test_status_code_other_error(self, mock_get):
        mock_get.side_effect = ValueError
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)
