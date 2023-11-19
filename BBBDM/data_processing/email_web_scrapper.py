import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pandas as pd

from BBBDM.data_processing.email_validator import validate_email

# Collins' web scraping function
def extract_email_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

    email_addresses = []
    for tag in soup.find_all('a'):
        email = tag.get('href')
        if email and 'mailto:' in email:
            clean_email = email.replace('mailto:', '')
            if clean_email not in email_addresses:
                email_addresses.append(clean_email)

    return email_addresses if email_addresses else None

# Integrated email verification function
def email_verification(website_url: str, historical_email: str, historical_name: str) -> list | None:
    emails = extract_email_data(website_url)
    if not emails:
        return None

    valid_emails = [email for email in emails if validate_email(historical_email, historical_name, email)]

    return valid_emails if valid_emails else None