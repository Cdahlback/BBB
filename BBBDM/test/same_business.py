import sys

# Add the project path to the system path for imports to work seamlessly
sys.path.append(r'C:\Users\tebib\OneDrive\Desktop\Project 1\BBB')

# Import the is_same_business function
from BBBDM.data_processing.Business_Match import is_same_business

def test_is_same_business():
    # Test cases for our function.
    # Cast strings and booleans as a demonstration of typecasting.
    test_cases = [
        (str("Bob's burgers"), str("Bob's burger and fries"), bool(True)),
        (str("coffee shop"), str("tea shop"), bool(False)),
        (str("MCDONALDS"), str("McDonald's"), bool(True)),
        (str("Wendys"), str("Wendy's Hamburgers"), bool(True)),
        (str("Dell Technologies"), str("Dell"), bool(True)),
        (str("Apple Store"), str("Apple Orchard"), bool(False))
    ]

    # Iterating through each test case
    for hist_name, new_name, expected in test_cases:
        result = is_same_business(hist_name, new_name)
        
        # Asserting that our function's result matches the expected result
        assert result == expected, f"Expected {expected} but got {result} for historical '{hist_name}' and new '{new_name}'"
    
    # If all assertions pass, this will print.
    print("All tests passed!")

# Run the test function
test_is_same_business()
