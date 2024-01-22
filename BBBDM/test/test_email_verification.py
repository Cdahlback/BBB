import sys
sys.path.append('C:/Users/tebib\OneDrive\Desktop\Project 1\BBB')  

from BBBDM.data_processing.email_verification import email_verification

 

def test_email_verification_with_real_company():
    # Website URL and known email from the website
    website_url = "https://www.godaddy.com/forsale/ablemovers.net"
    known_email = "arthurwilliamsoptical@gmail.com"
    historical_email = "arthurwilliamsoptical@gmail.com"

    # Run the email verification function with the provided website URL and historical email
    found_emails = email_verification(website_url, historical_email, None)  # Passing None for historical business name

    # Check if the known email is in the list of emails returned by your function
    assert known_email in found_emails, f"Test failed: {known_email} should be found on the website"

# Run the test function
if __name__ == "__main__":
    test_email_verification_with_real_company()