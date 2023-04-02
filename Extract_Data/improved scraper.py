import requests
import csv
from bs4 import BeautifulSoup
import re


def contains_business_name_in_copyright(html, business_name):
    """
    Check if the given business name is present in the footer of the website by comparing the number of matching words
    in the footer text and the business name. If at least 50% of the words in the business name are found in the footer
    text, the function returns True. Otherwise, it returns False.
    :param html: (BeautifulSoup object): The parsed HTML content of the website
    :param business_name: (str): The name of the business to search for
    :return: True if the business name is found in the footer of the website, False otherwise
    """
    if html is not None:
        try:
            # Find the footer element in the HTML
            footer = html.find('footer')

            # If footer is found, extract the text and count the number of matching words
            if footer is not None:
                footer_text = footer.text
                # extract all words from the footer text
                footer_text_words = re.findall(r'\b\w+\b', footer_text.lower())
                # extract all words from the business name
                business_name_words = re.findall(r'\b\w+\b', business_name.lower())
                matches = set(footer_text_words) & set(business_name_words)
                num_matches = len(matches)

                # Check if the number of matching words is at least 50% of the words in the business name
                if num_matches >= len(business_name_words) / 2:
                    return True
                else:
                    return False
            else:
                return False

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
        business_name = row['BusinessName']

        # Scrape the HTML from the website
        try:
            response = requests.get(website, timeout=10)
            html = BeautifulSoup(response.content, 'html.parser')

            # Check if the HTML contains the zip code
            if contains_business_name_in_copyright(html, business_name):
                print(f"Zip code {business_name} is found on {website}")
            else:
                print(f"Zip code {business_name} not found on {website}")

        except Exception as e:
            print(f"Error processing {website}: {e}")





