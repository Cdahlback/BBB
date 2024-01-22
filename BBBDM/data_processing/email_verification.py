import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pandas as pd


# Importing the validate_email function from the email_validator module
from BBBDM.data_processing.email_validator import validate_email

# Function to extract email addresses from a webpage
def extract_email_data(url):
    try:
        # Sending a GET request to the URL
        response = requests.get(url)
        # Parsing the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        # Printing any error that occurs during the request or parsing
        print(f"Error occurred: {e}")
        return None

    # List to hold extracted email addresses
    email_addresses = []
    # Looping through all 'a' tags (hyperlinks) in the HTML
    for tag in soup.find_all('a'):
        # Extracting the href attribute from each tag
        email = tag.get('href')
        # Checking if the href attribute contains an email address
        if email and 'mailto:' in email:
            # Removing the 'mailto:' part to get the clean email address
            clean_email = email.replace('mailto:', '')
            # Adding the email to the list if it's not already there
            if clean_email not in email_addresses:
                email_addresses.append(clean_email)

    # Returning the list of email addresses, or None if the list is empty
    return email_addresses if email_addresses else None

# Function to verify emails from a website against historical data

def email_verification(website_url: str, historical_email: str, historical_name: str):
    # Extracting emails from the website
    emails = extract_email_data(website_url)
    # If no emails are extracted, return None
    if not emails:
        return None

    # Validating each extracted email using the validate_email function
    valid_emails = [email for email in emails if validate_email(historical_email, historical_name, email)]

    # Returning the list of validated emails, or None if no emails are valid
    return valid_emails if valid_emails else None
