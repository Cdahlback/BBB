import unittest
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock

import requests
from Not_Our_Code.get_status_codes import status_code


class TestStatusCode(unittest.TestCase):

    def setUp(self):
        self.url = "http://www.example.com"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.timeout = 5

    @patch('Not_Our_Code.get_status_codes.requests.get')
    def test_status_code_success(self, mock_get):
        mock_get.return_value.status_code = 200
        self.assertEqual(status_code(self.url, self.headers, self.timeout), 200)

    @patch('Not_Our_Code.get_status_codes.requests.get')
    def test_status_code_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)

    @patch('Not_Our_Code.get_status_codes.requests.get')
    def test_status_code_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)

    @patch('Not_Our_Code.get_status_codes.requests.get')
    def test_status_code_other_error(self, mock_get):
        mock_get.side_effect = ValueError
        self.assertEqual(status_code(self.url, self.headers, self.timeout), -1)


# class test_generateUrl(unittest.TestCase):
#
#     def test_email_scraper(self):
#         id = 0
#         url1 = "http://www.mccallumconstruction.com/"
#         url2 = "http://beancounterstax.com/"
#
#         emails1 = data_extraction.extract_email_data(id, url1)
#         emails2 = data_extraction.extract_email_data(id, url2)
#
#         self.assertEqual(emails1, None)
#         self.assertEqual(emails2, {'BusinessID': 0, 'Email1': 'mailto:janell@beancounterstax.com', 'Email2': 'mailto:matt@beancounterstax.com', 'Email3': 'mailto:craig@beancounterstax.com'})
#
#     def test_statusCode(self):
#         url1 = "https://vetterhomes.com/"
#         url2 = "http://www.mnintegrity.com"
#         url3 = "https://www.ablemovingcorp.com/"
#
#         statusCode1 = generate_url.status_code(url1)
#         statusCode2 = generate_url.status_code(url2)
#         statusCode3 = generate_url.status_code(url3)
#
#         self.assertEqual(statusCode1, 200)
#         self.assertEqual(statusCode2, 404)
#         self.assertEqual(statusCode3, -1)

#
# if __name__ == '__main__':
#     unittest.main()