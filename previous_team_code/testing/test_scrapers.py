import unittest

import numpy as np
from Extract_Data.data_extraction import *

"""File used to test our independent variable scrapers for our machine learning model"""


class TestIndVarScrapers(unittest.TestCase):
    def test_url_contains_email(self):
        html = BeautifulSoup(
            '<html><body><a href="mailto:test@example.com">Test Email</a></body></html>',
            "html.parser",
        )
        email = "test@example.com"

        result = contains_email(html, email)
        self.assertTrue(result)

        result = contains_email(html, "notfound@example.com")
        self.assertFalse(result)

        result = contains_email(html, None)
        self.assertFalse(result)

        result = contains_email(None, email)
        self.assertIsNone(result)

    def test_url_contains_phone_number(self):
        html = BeautifulSoup(
            '<html><body><a href="tel:555-1234">555-1234</a></body></html>',
            "html.parser",
        )

        self.assertTrue(contains_phone_number(html, "555-1234"))

        self.assertFalse(contains_phone_number(html, "555-5678"))

        self.assertFalse(contains_phone_number(html, None))

        self.assertEqual(contains_phone_number(None, "555-1234"), np.nan)

    def test_contains_zipCode(self):
        html = BeautifulSoup(
            """
                    <html>
                      <body>
                        <p>Some text with a zip code 12345</p>
                        <p>Some more text with a zip code 67890</p>
                      </body>
                    </html>
                """,
            "html.parser",
        )

        self.assertTrue(contains_zipCode(html, "12345"))

        self.assertFalse(contains_zipCode(html, "54321"))

        self.assertFalse(contains_zipCode(html, None))

        self.assertEqual(contains_zipCode(None, "12345"), np.nan)

    def test_contains_reviews_page(self):
        # Test case where reviews page is found
        html = BeautifulSoup(
            '<html><body><a href="https://example.com/reviews">Reviews</a></body></html>',
            "html.parser",
        )
        self.assertTrue(contains_reviews_page(html))

        # Test case where reviews page is not found
        html = BeautifulSoup(
            '<html><body><a href="https://example.com/about">About Us</a></body></html>',
            "html.parser",
        )
        self.assertFalse(contains_reviews_page(html))

        # Test case where href attribute is None
        html = BeautifulSoup("<html><body><a>About Us</a></body></html>", "html.parser")
        self.assertFalse(contains_reviews_page(html))

    def test_contains_social_media_links(self):
        # Create a sample HTML page with social media links
        html = BeautifulSoup(
            """<html><head><title>Sample Page</title></head>
                    <body>
                        <a href="https://www.facebook.com">Facebook</a>
                        <a href="https://www.twitter.com">Twitter</a>
                        <a href="https://www.instagram.com">Instagram</a>
                        <a href="https://www.linkedin.com">LinkedIn</a>
                    </body>
                </html>""",
            "html.parser",
        )

        # Test that the function correctly identifies social media links
        self.assertTrue(contains_social_media_links(html))

        # Create a sample HTML page with no social media links
        html = BeautifulSoup(
            """<html><head><title>Sample Page</title></head>
                    <body>
                        <a href="https://www.example.com">Example</a>
                        <a href="https://www.google.com">Google</a>
                    </body>
                </html>""",
            "html.parser",
        )

        # Test that the function correctly identifies the absence of social media links
        self.assertFalse(contains_social_media_links(html))

        # Test that the function returns NaN for empty HTML input
        self.assertIsNone(contains_social_media_links(None))

    def test_contains_business_name_in_copyright(self):
        # Define the HTML content with the business name in the copyright section
        html_content = "<html><body><div>&copy; 2023, My Business Inc. All rights reserved.</div></body></html>"
        # Create a BeautifulSoup object from the HTML content
        html = BeautifulSoup(html_content, "html.parser")
        # Define the business name to look for
        business_name = "My Business"
        # Call the function and assert that it returns True
        self.assertTrue(contains_business_name_in_copyright(html, business_name))

        # Define the HTML content without the business name in the copyright section
        html_content = "<html><body><div>&copy; 2023, Another Business Inc. All rights reserved.</div></body></html>"
        # Create a BeautifulSoup object from the HTML content
        html = BeautifulSoup(html_content, "html.parser")
        # Define the business name to look for
        business_name = "My Business"
        # Call the function and assert that it returns False
        self.assertFalse(contains_business_name_in_copyright(html, business_name))

        # Define the HTML content as None
        html = None
        # Define the business name to look for
        business_name = "My Business"
        # Call the function and assert that it returns np.nan
        self.assertIsNone(contains_business_name_in_copyright(html, business_name))

        # Define the HTML content with the business name in the copyright section
        html_content = "<html><body><div>&copy; 2023, My Business Inc. All rights reserved.</div></body></html>"
        # Create a BeautifulSoup object from the HTML content
        html = BeautifulSoup(html_content, "html.parser")
        # Define the business name as None
        business_name = None
        # Call the function and assert that it returns False
        self.assertFalse(contains_business_name_in_copyright(html, business_name))

    def test_contains_business_name(self):
        html = BeautifulSoup(
            "<html><body><h1>Welcome to ABC's Company</h1></body></html>", "html.parser"
        )

        self.assertTrue(contains_business_name(html, "ABC's Company"))
        self.assertFalse(contains_business_name(html, "XYZ Inc."))

        self.assertIsNone(contains_business_name(None, "ABC Company"))

        self.assertFalse(contains_business_name(html, ""))

    def test_contains_contacts_page(self):
        # create valid html with a contact link
        html = BeautifulSoup(
            '<html><body><a href="contact">Contact Us</a></body></html>', "html.parser"
        )
        # test if the function returns True for the contact link
        self.assertTrue(contains_contacts_page(html))

        # create valid html without any contact link
        html = BeautifulSoup(
            '<html><body><a href="about">About Us</a></body></html>', "html.parser"
        )
        # test if the function returns False
        self.assertFalse(contains_contacts_page(html))

        # test if the function returns np.nan for None html
        self.assertIsNone(contains_contacts_page(None))

    def test_url_is_review_page(self):
        # create review page url for case 1
        c1_url = "https://www.yellowpages.com/mn/example-business/"
        # create review page url for case 2
        c2_url = "https://www.reviewpage.com/mn/companies/example-business/"
        # create review page html for case 3
        c3_html = BeautifulSoup(
            '<html><body><a href="review">Reviews</a></body></html>', "html.parser"
        )
        # create false test
        false_url = "https://www.examplebusiness.com/mankato/homepage/"
        false_html = BeautifulSoup(
            '<html><body><a href="contact">Contact Us</a></body></html>', "html.parser"
        )
        # run true/false tests
        self.assertTrue(url_is_review_page(c1_url, false_html))
        self.assertTrue(url_is_review_page(c2_url, false_html))
        self.assertTrue(url_is_review_page(false_url, c3_html))
        self.assertFalse(url_is_review_page(false_url, false_html))


class TestExtractData(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
