import unittest
import data_extraction

class test_generateUrl(unittest.TestCase):

    def test_email_scraper(self):
        id = 0
        url1 = "http://www.mccallumconstruction.com/"
        url2 = "http://beancounterstax.com/"

        emails1 = data_extraction.extract_email_data(id, url1)
        emails2 = data_extraction.extract_email_data(id, url2)

        self.assertEqual(emails1, None)
        self.assertEqual(emails2, {'BusinessID': 0, 'Email1': 'mailto:janell@beancounterstax.com', 'Email2': 'mailto:matt@beancounterstax.com', 'Email3': 'mailto:craig@beancounterstax.com'})

    def test_statusCode(self):
        url1 = "https://vetterhomes.com/"
        url2 = "http://www.mnintegrity.com"
        url3 = "https://www.ablemovingcorp.com/"

        statusCode1 = generate_url.status_code(url1)
        statusCode2 = generate_url.status_code(url2)
        statusCode3 = generate_url.status_code(url3)

        self.assertEqual(statusCode1, 200)
        self.assertEqual(statusCode2, 404)
        self.assertEqual(statusCode3, -1)


if __name__ == '__main__':
    unittest.main()