

from BBBDM.data_processing.email_web_scrapper import email_verification


def test_email_verification():
    # Successful Test Cases
    # Assuming these URLs and historical data should yield valid emails
    assert email_verification("http://successful-test-url-1.com", "valid@example.com", "Example Inc."), "Test failed: Valid email should be found"
    assert email_verification("http://successful-test-url-2.com", "contact@examplecorp.com", "Example Corp."), "Test failed: Valid email should be found"

    # Failed Test Cases
    # Assuming these URLs and historical data should not yield any valid emails
    assert email_verification("http://failed-test-url-1.com", "nonexistent@example.com", "Nonexistent Inc.") is None, "Test failed: No valid email should be found"
    assert email_verification("http://failed-test-url-2.com", "invalid@invalidcorp.com", "Invalid Corp.") is None, "Test failed: No valid email should be found"

# Run the test function
test_email_verification()
