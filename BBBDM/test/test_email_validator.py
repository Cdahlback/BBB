import sys
sys.path.append('C:/Users/tebib\OneDrive\Desktop\Project 1\BBB')  

# Test function for validate_email
# Assuming this test function is in a separate file and the email_validator module is correctly in your Python path
from email_validator import validate_email

def test_validate_email():
    # Historical email for comparison
    historical_email = "arthurwilliamsoptical@gmail.com"
    historical_name = None  # No historical business name 

    # Test cases for validate_email
    # Test with the same email - should pass
    assert validate_email(historical_email, historical_name, "arthurwilliamsoptical@gmail.com"), "Test failed: Exact email match"

    # Test with a different email but same domain - should pass
    assert validate_email(historical_email, historical_name, "differentuser@arthurwilliamsoptical.com"), "Test failed: Same domain, different user"

    # Test with a completely different email - should fail
    assert not validate_email(historical_email, historical_name, "user@differentdomain.com"), "Test failed: Completely different domain"

# Run the test function
if __name__ == "__main__":
    test_validate_email()
