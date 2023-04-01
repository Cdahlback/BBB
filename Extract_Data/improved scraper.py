import requests
import csv
from bs4 import BeautifulSoup
import re


def contains_zipcode(html, zipcode):
    """
        Check if the html contains the given zip code.
        :param html: html extracted from url
        :param zip_code: business zip code to find
        :return: True if the zip code is found in the html, False if not
        """
    if html is not None and zipcode is not None:
        try:
            # Look for zip code in the body of the HTML
            body_text = html.text.lower()
            zip_regex = re.compile(r'\b\d{5}\b')
            body_matches = zip_regex.findall(body_text)

            # If zip code not found in body, look in footer of the HTML
            if not body_matches:
                footer = html.find('footer')
                if footer is not None:
                    footer_text = footer.text.lower()
                    footer_matches = zip_regex.findall(footer_text)
                    body_matches += footer_matches

            # Check if the zip code is in the list of matches
            return str(zipcode) in body_matches
        except Exception as e:
            return False
    else:
        return False


# Open CSV file and read in data
with open('../data/sample.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Loop through each row in the CSV file
    for row in csv_reader:
        website = row['Website']
        zipcode = row['PostalCode']

        # Scrape the HTML from the website
        try:
            response = requests.get(website, timeout=10)
            html = BeautifulSoup(response.content, 'html.parser')

            # Check if the HTML contains the zip code
            if contains_zipcode(html, zipcode):
                print(f"Zip code {zipcode} found on {website}")
            else:
                print(f"Zip code {zipcode} not found on {website}")

        except Exception as e:
            print(f"Error processing {website}: {e}")





