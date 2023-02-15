from bs4 import BeautifulSoup

def has_business_name(soup, business_name):
    """Check if the soup contains the given business name."""
    # Find all text nodes in the soup
    for text in soup.find_all(text=True):
        # Check if the business name appears in the text
        if business_name.lower() in text.lower():
            return True
    # The business name was not found in the soup
    return False